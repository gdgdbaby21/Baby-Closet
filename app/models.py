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
    
    
#プロフィールのモデル
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
    
#欲しいものリストのモデル
class WishlistItem(models.Model):
    image = models.ImageField(upload_to='wishlist_images/', blank=True, null=True, default='wishlist_images/default.png')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    brand = models.CharField(max_length=50, blank=True)
    product_url = models.URLField(max_length=255, blank=True)
    notes = models.TextField(max_length=120, blank=True)

    def __str__(self):
        return f"{self.id} - {self.price}円"
    
    
#服管理画面のモデル
class Clothes(models.Model):
    GENDER_CHOICES = [
        ('Male', '男性'),
        ('Female', '女性'),
        ('Other', 'その他'),
    ]
    
    SIZE_CHOICES = [
        ('50~60', '50~60'),
        ('70', '70'),
        ('80', '80'),
        ('90', '90'),
        ('100', '100'),
        ('110', '110'),
        ('120', '120'),
        ('130', '130'),
        ('140', '140'),
    ]

    GENRE_CHOICES = [
        ('tops', 'トップス'),
        ('skirts', 'スカート'),
        ('outer', 'アウター'),
        ('onepiece', 'ワンピース'),
        ('pants', 'パンツ'),
        ('hat', '帽子'),
        ('maternity', 'マタニティ'),
        ('baby', 'ベビー'),
        ('other', 'その他'),
    ]

    COLOR_CHOICES = [
        ('white', '白'),
        ('black', '黒'),
        ('gray', 'グレー'),
        ('brown', '茶'),
        ('beige', 'ベージュ'),
        ('green', '緑'),
        ('blue', '青'),
        ('purple', '紫'),
        ('yellow', '黄'),
        ('pink', 'ピンク'),
        ('red', '赤'),
        ('orange', 'オレンジ'),
        ('other', 'その他'),
    ]

    title = models.CharField(max_length=50)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Unisex')
    color = models.CharField(max_length=10, choices=COLOR_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    memo = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='clothes_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.get_gender_display()} {self.size} {self.color} {self.genre}"
    

#ハッシュタグ検索のモデル  
class Hashtag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

#コーディネート投稿で使用したアイテムのモデル
class Item(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='items/images/')

    def __str__(self):
        return self.name


#コーディネート投稿のモデル
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/images/')
    title = models.CharField(max_length=50, default='Untitled')  
    caption = models.TextField(blank=True, null=True)
    # hashtags = models.ManyToManyField(Hashtag, blank=True)
    items = models.ManyToManyField(Item, blank=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.caption[:20]}'