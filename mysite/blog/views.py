from django.http import Http404
from django.shortcuts import render, get_object_or_404

# Create your views here.
from blog.models import Post


def post_list(request):
    posts = Post.published.all()
    context = {'posts': posts}
    return render(request, 'blog/list.html', context=context)


def post_datail(request, id):
    post = get_object_or_404(Post, id=id)
    context = {'post': post}
    return render(request, 'blog/datail.html', context=context)
