from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

@login_required
def upgrade(request):
    user = request.user
    gr = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        gr.user_set.add(user)
    return redirect('/')