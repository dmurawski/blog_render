from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render

from .models import Post


def post_list(request):
    post_list = Post.published.all()
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
    context = {"posts": posts}

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

    context = {"post": post}

    return render(
        request,
        "blog/post/detail.html",
        context,
    )
