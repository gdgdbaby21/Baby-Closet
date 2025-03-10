from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from .models import  User, WishlistItem, Clothes, Post, Comment
from django.core.exceptions import ValidationError
import re


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "password1", "password2", 'profile_image','account_name', 'gender', 'birth_of_date', 'bio']
        
        
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
    

User = get_user_model()

class UserProfileForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '新しいパスワード'}),
        required=False,
        label="新しいパスワード"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '新しいパスワード（確認）'}),
        required=False,
        label="新しいパスワード（確認）"
    )
    
    class Meta:
        model = User
        fields = ['email', 'profile_image', 'account_name', 'gender', 'birth_of_date', 'bio']
        labels = {
            'email': 'メールアドレス',
            'profile_image': 'プロフィール画像',
            'account_name': 'アカウント名',
            'gender': '性別',
            'birth_of_date': '生年月日',
            'bio': '自己紹介',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'account_name': forms.TextInput(attrs={'placeholder': 'アカウント名を入力してください'}),
            'gender': forms.Select(choices=[('M', '男性'), ('F', '女性'), ('O', 'その他')]),
            'birth_of_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'placeholder': '自己紹介を入力してください'}),
        }

    def clean_password1(self):
        password = self.cleaned_data.get("password1")

        if password:
            if len(password) < 8:
                raise ValidationError("パスワードは8文字以上である必要があります。")

            if not re.search(r"[a-z]", password):
                raise ValidationError("パスワードには少なくとも1つの小文字が必要です。")

            if not re.search(r"\d", password):
                raise ValidationError("パスワードには少なくとも1つの数字が必要です。")

        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password1 != password2:
            self.add_error("password2", "パスワードが一致しません。")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        email = self.cleaned_data.get("email")
        if email and email != user.email:
            user.email = email

        if self.cleaned_data.get("password1"):  
            user.set_password(self.cleaned_data["password1"])  

        if commit:
            user.save()

        return user
    
    
#欲しいものリスト投稿のフォーム        
class WishlistItemForm(forms.ModelForm):
    image = forms.ImageField(required=True)
    
    class Meta:
        model = WishlistItem
        fields = ['image', 'price','brand', 'product_url', 'notes']
        widgets = {
            'price': forms.NumberInput(attrs={
                'inputmode': 'numeric',  
                'pattern': '[0-9]*',  
                'onwheel': 'this.blur()',  
                'style': 'appearance: textfield; -moz-appearance: textfield;', 
                'class': 'custom-price-input',
            })
        }
        
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            raise forms.ValidationError("画像をアップロードしてください。")
        return image


#服管理検索ページのフォーム
class ClothingSearchForm(forms.Form):
    gender = forms.MultipleChoiceField(
        choices=Clothes.GENDER_CHOICES,
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        required=False
    )
    size = forms.MultipleChoiceField(
        choices=Clothes.SIZE_CHOICES,
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        required=False
    )
    color = forms.MultipleChoiceField(
        choices=Clothes.COLOR_CHOICES,
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        required=False
    )
    genre = forms.MultipleChoiceField(
        choices=Clothes.GENRE_CHOICES,
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        required=False
    )
    
#服管理のページのフォーム
class ClothingForm(forms.ModelForm):
    class Meta:
        model = Clothes
        fields = ['title', 'size', 'gender', 'color', 'genre', 'price', 'memo', 'image']
        widgets = {
            'price': forms.NumberInput(attrs={
                'inputmode': 'numeric',  
                'pattern': '[0-9]*', 
                'onwheel': 'this.blur()',  
                'style': 'appearance: textfield; -moz-appearance: textfield;', 
                'class': 'custom-price-input',  
            })
        }
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if not self.instance.image:
                self.fields['image'].initial = 'default.jpg'
        
        # ✅ 画像がアップロードされているかチェック
        def clean_image(self):
            image = self.cleaned_data.get('image')
            if not image:
                raise forms.ValidationError("画像登録してください")  # 🔥 画像がない場合にエラーメッセージを返す
            return image


#コーディネート投稿のフォーム
class PostForm(forms.ModelForm):
      is_public = forms.BooleanField(required=False) 
      clothes = forms.ModelMultipleChoiceField(
        queryset=Clothes.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="関連する服"
    )
      class Meta:
        model = Post
        fields = ['title', 'caption', 'image', 'is_public', 'clothes']
        widgets = {
            'caption': forms.Textarea(attrs={
                'placeholder': 'メモ・ハッシュタグを入力してください',
                'rows': 3
            }),
            'title': forms.TextInput(attrs={
                'placeholder': 'タイトルを入力してください'
            }),
        }
        
#コメントのフォーム
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user', 'content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'コメントを入力してください...',
                'rows': 3,
                'style': 'resize:none;'
            }),
        }
        labels = {
            'content': '',
        }