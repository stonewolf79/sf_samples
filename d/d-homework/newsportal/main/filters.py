
from django_filters import FilterSet
from .models import Post

# d7 Критерии должны быть следующие:
# по названию
# по тегу ??? откуда теги взялись
# позже указываемой даты
class PostFilter(FilterSet):
	class Meta:
		model = Post
		fields = { 'title': ['icontains'], 'created': ['gte'] }
