from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView, DetailView, CreateView, UpdateView, DeleteView)
from django.urls import reverse_lazy, reverse


# Create your views here.

# baza stron, taka topka
def PostListView(request):
    post_list = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    post_dict = {'post_list': post_list}
    return render(request, 'blog_app/post_list.html', context=post_dict)


# krótkie about
class About(TemplateView):
    template_name = 'blog_app/about.html'


# tworzenie nowych postów
class CreatePost(LoginRequiredMixin, CreateView):
    template_name = 'blog_app/post.html'
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm
    model = Post


class PostDetail(DetailView):
    model = Post


class PostEdit(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    template_name = 'blog_app/post.html'
    redirect_field_name = 'blog_app/post_detail.html'
    model = Post
    form_class = PostForm


class PostDelete(LoginRequiredMixin, DeleteView):
    template_name = 'blog_app/post_delete.html'
    model = Post
    success_url = reverse_lazy('post_list')


@login_required
def publish_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
def approve_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


# TODO:Działające lajki
@login_required
def give_like(request, pk):
   post = get_object_or_404(Post, id=request.POST.get('post_id'))
   post.likes.add(request.user)
   return redirect('post_list')


def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog_app/comment.html', {'form': form})


@login_required
def remove_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)
