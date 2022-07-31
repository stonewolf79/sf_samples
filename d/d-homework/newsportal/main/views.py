from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import *
from .filters import *

class NewsList(ListView):
    model = Post
    ordering = 'created'
    template_name = 'news.html'
    context_object_name = 'news' # переменная в шаблоне
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        print(1,self.filterset)
        return self.filterset.qs
		
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        print(2,self.filterset)
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
