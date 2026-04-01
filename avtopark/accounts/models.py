from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('user', 'Foydalanuvchi'),
        ('admin', 'Admin'),
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')
    phone = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=200)
    address = models.TextField(blank=True, null=True)
    passport_series = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.full_name} ({self.phone})"
    
    def is_admin_user(self):
        return self.user_type == 'admin' or self.is_staff