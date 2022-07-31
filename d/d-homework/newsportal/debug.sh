#!/bin/bash

echo ""
echo "база данных:"

shell='python manage.py shell -c'

$shell "from django.contrib.auth.models import User as cls;print(list(cls.objects.all()))"
$shell "from main.models import Author as cls;print(list(cls.objects.all()))"
$shell "from main.models import Category as cls;print(list(cls.objects.all()))"
$shell "from main.models import Post as cls;print(list(cls.objects.all()))"
$shell "from main.models import Comment as cls;print(list(cls.objects.all()))"
