from datetime import datetime
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(unique=True, max_length=255, default='без категории')

    def __str__(self):
        return f'{self.name}'

postType = [('A','article'),('N','news')]

class PostCategory(models.Model):
    pst = models.ForeignKey('Post', on_delete=models.CASCADE)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE)

class Post(models.Model):

    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default='')
    text = models.TextField(default='')
    rating = models.IntegerField(default=0)
    pType = models.CharField(max_length=1, choices=postType, default='A')
    cat = models.ManyToManyField(Category, through='PostCategory')
    created = models.DateTimeField(auto_now_add=True)

    def init(self, authorName:str, cats:str):
        ''' установка автора и категорий '''
        author = Author.find(name=authorName)
        if author: self.author = author

        sneedCat = cats.split(',')
        catref = {_.name:_ for _ in list(Category.objects.all())}
        catlist = [v for k,v in catref.items() if k in sneedCat]
        self.save()
        self.cat.set(catlist)
        self.save()

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    @property
    def preview(self):
        return f'{self.text[:124]}…'

    def __str__(self):
        authorName = self.author.user.username
        #return '' # заглушка для отладки
        return f'{authorName} - тип {self.pType} рейтинг={self.rating} - {list(self.cat.all())} - "{self.title[:20]}..." - "{self.text[:20]}..."'

    def get_absolute_url(self):
        if self.pType=='A': name = 'articles'
        else: name = 'news'
        #r = reverse(name, args=[self.pk]) # не работает
        #r = reverse(name, kwargs={'pk':self.pk}) # не работает
        r = f'/{name}/{self.pk}'
        return r


class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(default='')
    created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def init(self, postnum, user, text):
        self.post = Post.objects.all()[postnum]
        self.user = User.objects.filter(username=user)[0]
        self.text = text
        self.save()

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        sdate = self.created.strftime("%y.%m.%d %H:%M:%S")
        return f'{self.user.username} - R={self.rating} - {sdate} - "{self.text[:20]}..."'
    
class Author(models.Model):

    # напрашивается поле name, но его нет в задании, поэтому имя тягаем из пользователя
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    @property
    def name(self):
        return self.user.username

    @staticmethod
    def find(name:str):
        ''' найти автора по имени пользователя '''
        musr = list(User.objects.filter(username=name))
        if musr: 
            ma = Author.objects.filter(user=musr[0])
            if ma: return ma[0]
        return None

    def __str__(self):
        return f'{self.name} = {self.rating}'

    def set_user(self, name):
        musr = list(User.objects.filter(username=name))
        if musr:
            self.user=musr[0]
            self.save()
    
    def update_rating(self):
        r = sum([_.rating for _ in Post.objects.filter(author=self)]) * 3 # суммарный рейтинг каждой статьи автора умножается на 3
        r += sum([_.rating for _ in Comment.objects.filter(user=self.user)]) # суммарный рейтинг всех комментариев автора
        r += sum([_.rating for _ in Comment.objects.filter(post__author=self)]) # суммарный рейтинг всех комментариев к статьям автора
        self.rating = r
        self.save()

    @staticmethod
    def calc_rating():
        ma = list(Author.objects.all())
        for a in ma: a.update_rating()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    google = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username}'