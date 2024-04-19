from django.db import models
from django.contrib.auth.models import AbstractUser

from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    username = models.CharField(max_length=18, unique=True, null=True, blank=True, validators=[phone_regex])
    avatar = models.ImageField(upload_to='avatar/', null=True, blank=True)


class BlacklistedToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    token = models.CharField(max_length=255, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Blacklisted Token"
        verbose_name_plural = "Blacklisted Tokens"

    def __str__(self):
        return f"{self.user.username}'s Token"