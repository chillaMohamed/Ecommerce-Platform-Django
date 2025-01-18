
from django.urls import path
from django.contrib.auth.urls import urlpatterns
from django.contrib.auth.views import LoginView

from .views import signup_view, activate_view, profile_view

app_name = 'accounts'

urlpatterns = urlpatterns + [
    path('signup/', signup_view, name='signup'),
    path('activate/<uid>/<token>/', activate_view, name='activate'),
    path('profile/', profile_view, name='profile'),
]