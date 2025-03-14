from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
import re
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.templatetags.static import static



#ユーザー登録のモデル
class User(AbstractUser):
    first_name = None
    last_name = None
    date_joined = None
    groups = None
    user_permissions = None
    username = None
    

    email = models.EmailField(max_length=50, unique=True)
    account_name = models.CharField(max_length=50, unique=True, default="")
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('male', '男性'), ('female', '女性'), ('other', 'その他')], default="other")
    birth_of_date = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []
    
    class Meta:
        db_table = "users"
    


#欲しい服リストのモデル
class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='wishlist_images/', null=False, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    brand = models.CharField(max_length=50, blank=True)
    product_url = models.URLField(max_length=255, blank=True)
    notes = models.TextField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.price}円"
    
    


#ハッシュタグ検索のモデル  
class Hashtag(models.Model):  
   user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
   name = models.CharField(max_length=50, unique=True)
   popularity = models.IntegerField(default=0)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)
   
   def __str__(self):
        return self.word


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
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Unisex')
    color = models.CharField(max_length=10, choices=COLOR_CHOICES)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    memo = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='clothes_images/', null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_gender_display()} {self.size} {self.color} {self.genre}"
    
    def get_related_posts(self):
        return self.posts.all()
    
    def get_image_url(self):
        """画像が未登録の場合、デフォルト画像（static）を返す"""
        if self.image:
            return self.image.url
        return static('images/default-clothes.png')


    

#コーディネート投稿のモデル
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    clothes = models.ManyToManyField(Clothes, related_name='posts', blank=True)
    hashtags = models.ManyToManyField(Hashtag, related_name='posts') 
    image = models.ImageField(upload_to='posts/images/')
    title = models.CharField(max_length=50, default='')
    is_public = models.BooleanField(default=False)
    caption = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.caption:
            hashtags = set(re.findall(r"#(\w+)", self.caption))
            for tag_name in hashtags:
                hashtag, created = Hashtag.objects.get_or_create(name=tag_name)
                self.hashtags.add(hashtag)

# プロパティでいいね数を取得
    @property
    def likes_count(self):
        return self.likes.count()

    # プロパティでコメント数を取得
    @property
    def comments_count(self):
        return self.comments.count()



#いいね機能のモデル
User = get_user_model()

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"


#コメント機能のモデル
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"