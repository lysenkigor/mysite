from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView

from blog.forms import EmailForm, CommentForm
from blog.models import Post, Comment


# def post_list(request):
#     post_list = Post.objects.all()
#     paginator = Paginator(post_list, 1)
#     page_number = request.GET.get('page', 1)
#     try:
#         posts = paginator.page(page_number)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     context = {'posts': posts}
#     return render(request, 'blog/list.html', context=context)

class PostList(ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/list.html'


def post_detail(request, year, month, day, post_slug):
    post = get_object_or_404(Post,
                             slug=post_slug,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True, parent_comment=None)
    form = CommentForm()
    context = {'post': post, 'comments': comments, 'form': form}
    return render(request, 'blog/post_detail_page.html', context=context)


# class PostDetail(DetailView):
#     model = Post
#     template_name = 'blog/post_detail_page.html'

def form_page(request):
    if request.method == 'POST':
        print('post')
        form = EmailForm(request.POST)
        if form.is_valid():
            print('form valid')
            return HttpResponseRedirect('/')
    else:
        form = EmailForm()
    return render(request, 'blog/form.html', {'form': form})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    # context = {'post': post, 'form': form, 'comment': comment}
    return redirect('post_detail', post.publish.year, post.publish.month, post.publish.day, post.slug)


def add_dependent_comment(request, post_id, parent_comment_id):
    parent_comment = get_object_or_404(Comment, id=parent_comment_id)
    post = get_object_or_404(Post, id=post_id)
    dependent_comment = None
    if request.method == 'GET':
        return render(request, 'blog/includes/dep_comment_form.html', context={'form': CommentForm(),
                                                                               'post': post,
                                                                               'parent_comment': parent_comment})
    else:
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.parent_comment = parent_comment
            comment.post = parent_comment.post
            comment.save()
            return redirect('post_detail', post.publish.year, post.publish.month, post.publish.day, post.slug)
        # print(form.er)
        return render(request, 'blog/includes/dep_comment_form.html', context={'form': CommentForm(),
                                                                               'post': post,
                                                                               'parent_comment': parent_comment,
                                                                               'form_errors': form.errors})


def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post = get_object_or_404(Post, id=post_id)
    comment.delete()
    return redirect('post_detail', post.publish.year, post.publish.month, post.publish.day, post.slug)


def update_comment(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'GET':
        form = CommentForm(instance=comment)
        return render(request, 'blog/includes/update_comment.html', {'post': post,
                                                                     'comment': comment,
                                                                     'form': form})
    else:
        try:
            form = CommentForm(request.POST, instance=comment)
            form.save()
            return redirect('post_detail', post.publish.year, post.publish.month, post.publish.day, post.slug)
        except ValueError:
            form = CommentForm(instance=comment)
            return render(request, 'blog/includes/update_comment.html', {'post': post,
                                                                         'comment': comment,
                                                                         'form': form,
                                                                         'error': 'Incorrect data in the form'})
