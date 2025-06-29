from django.shortcuts import render, get_object_or_404
from .models import Post
from .utils import bubble_sort

def post_list(request):
    query = request.GET.get("q", "").strip()
    sort  = request.GET.get("sort", "id")

    qs = Post.objects.all()
    if query:
        qs = qs.filter(title__icontains=query)

    posts = list(qs)   # Django-QuerySet → python-list для алгоритма
    if sort == "title":
        posts = bubble_sort(posts, key=lambda p: p.title.lower())
    else:              # default → sort by id
        posts = bubble_sort(posts, key=lambda p: p.id)

    ctx = {"posts": posts, "query": query, "sort": sort}
    return render(request, "posts/list.html", ctx)


def post_detail(request, pk: int):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "posts/detail.html", {"post": post})
