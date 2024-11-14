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
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    name = models.CharField(max_length=100)
    account = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=[('male', '男性'), ('female', '女性')])
    birth_of_date = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    
    
    def __str__(self):
        return f"{self.user.username}'s profile"
    
#欲しいものリストの投稿情報保存のモデルの作成
class WishlistItem(models.Model):
    image = models.ImageField(upload_to='wishlist_images/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    brand = models.CharField(max_length=50, blank=True)
    product_url = models.URLField(max_length=255, blank=True)
    notes = models.TextField(max_length=120, blank=True)

    def __str__(self):
        return f"{self.id} - {self.price}円"