#!/bin/bash

#   домашка d 5.9

# очистка базы
if [ -f clean.sh ];then ./clean.sh;fi

shell='python manage.py shell -c'

# 1 Создать двух пользователей (с помощью метода User.objects.create_user('username')).
$shell "from django.contrib.auth.models import User;User.objects.create_user('user1')"
$shell "from django.contrib.auth.models import User;User.objects.create_user('user2')"
$shell "from django.contrib.auth.models import User;User.objects.create_user('user3')" # не автор
$shell "from django.contrib.auth.models import User;User.objects.create_user('user4')" # не автор

# 2 Создать два объекта модели Author, связанные с пользователями.
$shell "from main.models import Author as cls;o=cls();o.set_user('user1')"
$shell "from main.models import Author as cls;o=cls();o.set_user('user2')"

# 3 Добавить 4 категории в модель Category.
$shell "from main.models import Category as cls;o=cls.objects.create(name='IT');"
$shell "from main.models import Category as cls;o=cls.objects.create(name='политика');"
$shell "from main.models import Category as cls;o=cls.objects.create(name='религия');"
$shell "from main.models import Category as cls;o=cls.objects.create(name='ктулхуведение');"

# 4 Добавить 2 статьи и 1 новость.
# 5 Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
title='правильное использование шаманского бубна при отладке'
cat='IT,ктулхуведение'
$shell "from main.models import Post as cls;o=cls(title='$title',pType='A',text='текст1');o.init('user1','$cat')"

title='как пофиксить все баги и не сломать клавиатуру'
cat='IT'
$shell "from main.models import Post as cls;o=cls(title='$title',pType='A',text='текст поста2 редиска РеДиСкА конецпоста');o.init('user1','$cat')"

title='деревенский программист написал на пайтон операционную систему и открыл портал в ад'
cat='IT,политика,религия'
$shell "from main.models import Post as cls;o=cls(title='$title',pType='N',text='редиска РеДиСкА конецновости');o.init('user2','$cat')"

# 30шт новостей для теста пагинатора d7
cat='IT,политика,религия'
for ((n=1;n<=30;n++));do
    #echo "добавление новости #$n"
    title="тестовая новость пагинатора #$n"
    text="текст для новости пагинатора #$n"
    $shell "from main.models import Post as cls;o=cls(title='$title',pType='N',text='$text');o.init('user2','$cat')"
done

# 6 Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).
$shell "from main.models import Comment as cls;o=cls();o.init(postnum=0,user='user1',text='comment1')"
$shell "from main.models import Comment as cls;o=cls();o.init(postnum=1,user='user2',text='comment2 редиска РеДиСкА конецкоммента')"
$shell "from main.models import Comment as cls;o=cls();o.init(postnum=2,user='user3',text='comment3')"
$shell "from main.models import Comment as cls;o=cls();o.init(postnum=0,user='user4',text='comment4')"

# 7 Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
$shell "from main.models import Comment as cls;o=cls.objects.all()[0].like()"
$shell "from main.models import Comment as cls;o=cls.objects.all()[1].like()"
$shell "from main.models import Comment as cls;o=cls.objects.all()[2].dislike()"
$shell "from main.models import Comment as cls;o=cls.objects.all()[3].dislike()"

$shell "from main.models import Post as cls;o=cls.objects.all()[0].like()"
$shell "from main.models import Post as cls;o=cls.objects.all()[1].dislike()"
$shell "from main.models import Post as cls;o=cls.objects.all()[2].like()"

# 8 Обновить рейтинги пользователей.
$shell "from main.models import Author as cls;cls.calc_rating()"

# 9 Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
$shell "from main.models import Author as cls;\
    print('лучший пользователь:',cls.objects.order_by('-rating').values('user__username','rating').first())"

# 10 Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье.
# 11 Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
$shell "from main.models import Post,Comment;\
    bestPost = Post.objects.order_by('-rating')[0];\
    print(f'лучший пост: автор: {bestPost.author.name} рейтинг: {bestPost.rating} заголовок: \"{bestPost.title}\" превью: \"{bestPost.preview}\"');\
    mcom = list(Comment.objects.filter(post=bestPost).values('created','user__username','rating','text'));\
    print('комментарии лучшего поста:', mcom);\
    "

# посмотрим что там у нас в базе...
if [ -f debug.sh ];then ./debug.sh;fi
