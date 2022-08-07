from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from main.views import RegView

from sign.views import upgrade

urlpatterns = [
    path('login/', LoginView.as_view(template_name = 'login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name = 'logout.html'), name='logout'),
    path('reg/', RegView.as_view(template_name = 'reg.html'), name='reg'),
    path('upgrade/', upgrade, name = 'upgrade')
]
