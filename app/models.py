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
    
#Postモデルとハッシュタグモデルの作成
class Hashtag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"#{self.name}"

class Post(models.Model):
    content = models.TextField()
    hashtags = models.ManyToManyField(Hashtag, blank=True, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content