from django.shortcuts import get_object_or_404, render

from .models import Post


def post_list(request):
    posts = Post.published.all()
    context = {"posts": posts}

    return render(
        request,
        "blog/post/list.hmtl",
        context,
    )


def post_detail(request, id):
    posts = get_object_or_404(
        Post,
        id,
        status=Post.Status.PUBLISHED,
    )
    context = {"posts": posts}

    return render(
        request,
        "blog/post/detail.hmtl",
        context,
    )
