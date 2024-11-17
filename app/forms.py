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
        

class ClothingSearchForm(forms.Form):
    GENDER_CHOICES = [
        ('male', '男'),
        ('female', '女'),
    ]
    SIZE_CHOICES = [
        ('50-60', '50-60'),
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
        ('white', '白'),
        ('gray', 'グレー'),
        ('blue', '青'),
        ('green', '緑'),
        ('red', '赤'),
        ('yellow', '黄'),
        ('pink', 'ピンク'),
        ('orange', 'オレンジ'),
        ('other', 'その他'),
    ]
    GENRE_CHOICES = [
        ('tops', 'トップス'),
        ('skirt', 'スカート'),
        ('outer', 'アウター'),
        ('onepiece', 'ワンピース'),
        ('pants', 'パンツ'),
        ('hat', '帽子'),
        ('maternity', 'マタニティ'),
        ('other', 'その他'),
    ]

    gender = forms.ChoiceField(choices=[('', '選択')] + GENDER_CHOICES, widget=forms.Select, required=False)
    size = forms.MultipleChoiceField(choices=SIZE_CHOICES, widget=forms.SelectMultiple(attrs={'size': 5}), required=False)
    color = forms.MultipleChoiceField(choices=COLOR_CHOICES, widget=forms.SelectMultiple(attrs={'size': 5}), required=False)
    genre = forms.ChoiceField(choices=[('', '選択')] + GENRE_CHOICES, widget=forms.Select, required=False)
