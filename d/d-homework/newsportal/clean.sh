#!/bin/bash

shell='python manage.py shell -c'

$shell "from django.contrib.auth.models import User;User.objects.all().delete()"
$shell "from main.models import Author as cls;cls.objects.all().delete()"
$shell "from main.models import Category as cls;cls.objects.all().delete()"
$shell "from main.models import Post as cls;cls.objects.all().delete()"
$shell "from main.models import Comment as cls;cls.objects.all().delete()"
