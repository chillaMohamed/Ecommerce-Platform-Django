from django.conf import settings
from django.core.validators import EmailValidator, RegexValidator
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, BaseUserManager


COUNTRY_CHOICES = [
    ('US', 'United States'),
    ('CA', 'Canada'),
    ('FR', 'France'),
    ('DE', 'Germany'),
    ('GB', 'United Kingdom'),
    ('DZ', 'Algeria'),
    # Add more countries as needed
]

def get_default_user_verification_settings():
    return not getattr(settings, 'USER_ACCOUNT_ACTIVATION', False)

class CustomUser(AbstractUser):
    # Override the username field to enforce email format
    username = models.CharField(
        verbose_name=_("Email Address"),
        max_length=150,
        unique=True,
        validators=[EmailValidator(message="Enter a valid email address.")],
        help_text="Required. 150 characters or fewer. Must be a valid email address.",
    )

    country = models.CharField(
        verbose_name=_("Country"),
        max_length=30,
        choices=COUNTRY_CHOICES,
        default='DZ',
        null=True,
        blank=True,
    )

    phone = models.CharField(
        verbose_name=_("Phone"),
        max_length=15,
        unique=True,
        validators=[
            RegexValidator(regex=r'^\+?1?\d{9,15}$', message=_("Enter a valid phone number."))
        ],
        blank=True,  # optional field, set to False if phone is required
        null=True  # allow NULL values in the database
    )

    is_active = models.BooleanField(
        _("active"),
        default= get_default_user_verification_settings,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    @property
    def email(self):
        return self.username

    @email.setter
    def email(self, value):
        pass

    @property
    def full_name(self):
        return (self.first_name+" "+self.last_name).lower()

    EMAIL_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Ensure superusers are always active
        if self.is_superuser:
            self.is_active = True
        super().save(*args, **kwargs)
