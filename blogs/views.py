from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from . models import Post
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.core.paginator import Paginator





def Home(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'blogs/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blogs/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3

    def get_context_data(self, **kwargs):
        # get the default context (Django’s own stuff)
        context = super().get_context_data(**kwargs)
        
        # get the page object from the context
        page_obj = context['page_obj']

        # calculate custom range
        page_number = page_obj.number
        paginator = page_obj.paginator
        custom_range = range(
            max(1, page_number - 3),
            min(page_number + 3, paginator.num_pages) + 1
        )

        # add it to the context
        context['custom_range'] = custom_range
        return context


class UserPostListView(ListView):
    model = Post
    template_name = 'blogs/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostView(DetailView):
    model = Post
    template_name = 'blogs/post_detail.html'
    context_object_name = 'post' 

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blogs/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form) 

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blogs/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)  

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False 
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin ,DeleteView):
    model = Post
    template_name = 'blogs/post_delete.html'
    context_object_name = 'post' 
    success_url = reverse_lazy('home')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False 

def About(request):
    return render(request, 'blogs/about.html')


