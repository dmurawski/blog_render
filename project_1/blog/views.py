from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Post


def post_list(request):
    post_list = Post.published.all()
    # paginate
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get("page", 1)
    posts = paginator.page(page_number)

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
