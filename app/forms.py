from django import forms
from django.contrib.auth.forms import UserCreationForm
from app.models import User
from django.contrib.auth import authenticate
from .models import UserProfile, WishlistItem, Clothes
import datetime


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("このメールアドレスは既に登録されています")
        return email
    
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()
    
    
    def clean(self):
        print("loginformのクリーンが呼び出された")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        print(email, password)
        self.user = authenticate(email=email, password=password)
        if self.user is None:
            raise forms.ValidationError("認証に失敗しました")
        return self.cleaned_data
    


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image','name','account', 'gender', 'birth_of_date', 'bio']
        labels = {
            'profile_image': 'プロフィール画像',
            'name': '名前',
            'account': 'アカウント名',
            'gender': '性別',
            'birth_of_date': '生年月日',
            'bio': '自己紹介',
        }
        widgets = {
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '名前を入力'}),
            'account': forms.TextInput(attrs={'placeholder': 'フリー入力'}),
            'gender': forms.Select(choices=[('M', '男性'), ('F', '女性'), ('O', 'その他')]),
            'birth_of_date': forms.SelectDateWidget(years=range(1900, 2024)),
            'bio': forms.Textarea(attrs={'placeholder': 'フリー入力'}),
        }



#欲しいものリスト投稿のフォーム        
class WishlistItemForm(forms.ModelForm):
    class Meta:
        model = WishlistItem
        fields = ['image', 'price','brand', 'product_url', 'notes']
        

#服管理のフォーム
class ClothesForm(forms.ModelForm):
    class Meta:
        model = Clothes
        fields = ['title', 'size', 'gender', 'genre', 'color', 'price', 'memo', 'image']
        

#服管理検索ページのフォーム
class ClothesSearchForm(forms.Form):
    GENDER_CHOICES = [
        ('', '選択'),
        ('Male', '男性'),
        ('Female', '女性'),
    ]
    
    SIZE_CHOICES = [
        ('', '選択'),
        ('50-60', '50~60'),
        ('70', '70'),
        ('80', '80'),
        ('90', '90'),
        ('100', '100'),
        ('110', '110'),
        ('120', '120'),
        ('130', '130'),
        ('140', '140'),
    ]
    
    COLOR_CHOICES = [
        ('', '選択'),
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
    
    GENRE_CHOICES = [
        ('', '選択'),
        ('tops', 'トップス'),
        ('skirts', 'スカート'),
        ('outer', 'アウター'),
        ('onepiece', 'ワンピース'),
        ('pants', 'パンツ'),
        ('hat', '帽子'),
        ('maternity', 'マタニティ'),
        ('other', 'その他'),
    ]

    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        required=False,
        label='性別'
    )
    size = forms.ChoiceField(
        choices=SIZE_CHOICES,
        required=False,
        label='サイズ'
    )
    color = forms.ChoiceField(
        choices=COLOR_CHOICES,
        required=False,
        label='カラー'
    )
    genre = forms.ChoiceField(
        choices=GENRE_CHOICES,
        required=False,
        label='ジャンル'
    )