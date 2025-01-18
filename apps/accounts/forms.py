
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class CustomUserRegisterForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username","first_name","last_name", "country", "password1", "password2")
