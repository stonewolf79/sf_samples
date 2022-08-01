from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import *
from .filters import *
from .forms import *

class NewsList(ListView):
    model = Post
    ordering = 'created'
    template_name = 'news.html'
    context_object_name = 'news' # переменная в шаблоне
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        #print(1,self.filterset)
        return self.filterset.qs
		
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        #print(2,self.filterset)
        return context

class PostList(ListView):
    model = Post
    ordering = '-created'
    template_name = 'posts.html'
    context_object_name = 'posts' # переменная в шаблоне

class PostInfo(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'info' # переменная в шаблоне

class PostCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'

    def get_success_url(self, **kwargs):
        name = self.request.path.split('/')[1]
        return reverse_lazy(name)

class PostEdit(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'

class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    context_object_name = 'info' # переменная в шаблоне
    success_url = reverse_lazy('news')

    def get_success_url(self, **kwargs):
        name = self.request.path.split('/')[1]
        return reverse_lazy(name)
