from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import Http404
from django.views import generic
from braces.views import SelectRelatedMixin
from django.contrib import messages
from . import models
from . import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
User = get_user_model()

# Create your views here.

class PostList(SelectRelatedMixin,generic.ListView):
    model = models.Post
    select_related = ('user','group')

class UserPosts(generic.ListView):
    model = models.Post
    template_name = 'posts/user_posts_list.html'

    def get_queryset(self):
        try: 
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, *args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['post_user'] = self.post_user
        return context

class PostDetail(SelectRelatedMixin,generic.DetailView):
    model = models.Post 
    select_related = ('user','group')
     
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user__username__iexact=self.kwargs.get('username'))
        return queryset


class CreatePost(LoginRequiredMixin,SelectRelatedMixin,generic.CreateView):

    fields = ('title','message', 'group')
    model = models.Post

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class DeletePost(LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):
    model = models.Post
    select_related = ('user', 'group')
    success_url = reverse_lazy('posts:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user_id=self.request.user.id)
        return queryset 
    def delete(self,*args,**kwargs):
        messages.success (self.request, 'Post Deleted')
        return super().delete(*args,**kwargs)   
