from django.contrib.postgres.search import SearchVector
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from taggit.models import Tag

from .forms import CommentForm, EmailPostForm, SearchForm
from .models import Post


def post_share(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED,
    )
    sent = False

    if request.method == "POST":
        form = EmailPostForm(request.POST, post_id=post.id)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = (
                f"{cd['name']} ({cd['email']}) " f"recommends you read {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}'s comments: {cd['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd["to"]],
            )
            sent = True
    else:
        form = EmailPostForm(post_id=post.id)

    return render(
        request,
        "blog/post/share.html",
        {
            "post": post,
            "form": form,
            "sent": sent,
        },
    )


def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    # paginate
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # return first page
        posts = paginator.page(1)
    except EmptyPage:
        # return last page
        posts = paginator.page(paginator.num_pages)

    context = {"posts": posts, "tag": tag}

    return render(
        request,
        "blog/post/list.html",
        context,
    )


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    # list of active commnets for post

    comments = post.comments.filter(active=True)
    form = CommentForm()

    # List of smiliar posts
    # list of id for tags of current post [1,2,3,4,....]
    post_tags_ids = post.tags.values_list("id", flat=True)
    smiliar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = smiliar_posts.annotate(same_tags=Count("tags")).order_by(
        "-same_tags",
        "-publish",
    )[:4]

    context = {
        "post": post,
        "comments": comments,
        "form": form,
        "similar_posts": similar_posts,
    }

    return render(
        request,
        "blog/post/detail.html",
        context,
    )


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    return render(
        request,
        "blog/post/comment.html",
        {
            "post": post,
            "form": form,
            "comment": comment,
        },
    )


def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            results = Post.published.annotate(
                search=SearchVector("title", "body")
            ).filter(search=query)

    return render(
        request,
        "blog/post/search.html",
        {
            "form": form,
            "results": results,
            "query": query,
        },
    )
