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
    ユーザー = models.OneToOneField(User, on_delete=models.CASCADE)
    画像 = models.ImageField(upload_to='avatars/', null=True, blank=True)
    アカウント名 = models.CharField(max_length=50)
    性別 = models.CharField(max_length=10, choices=[('male', '男性'), ('female', '女性')])
    生年月日 = models.DateField(null=True, blank=True)
    自己紹介 = models.TextField(max_length=500, blank=True)
    
    
    def __str__(self):
        return self.user.username
    
class WishlistItem(models.Model):
    image = models.ImageField(upload_to='wishlist_images/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.CharField(max_length=255)
    product_url = models.URLField()
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.brand