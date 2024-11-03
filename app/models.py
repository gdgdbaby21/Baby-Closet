from django.db import models
from django.contrib.auth.models import AbstractUser




class User(AbstractUser):
    first_name = None
    last_name = None
    date_joined = None
    groups = None
    user_permissions = None
    
    
username = models.CharField(max_length=50, unique=True)
email = models.EmailField(max_length=50, unique=True)
created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)


USERNAME_FIELD = "username"
EMAIL_FIELD = "email"
REQUIRED_FIELDS = ["email"]

class Meta:
    db_table = "users"
    
    
#プロフィール情報の管理するモデルの作成
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    account_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    
    
    def __str__(self):
        return self.user.username