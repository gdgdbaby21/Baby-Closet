from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import  User, WishlistItem, Clothes, Post, Comment


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
    


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_image','account_name', 'gender', 'birth_of_date', 'bio']
        labels = {
            'profile_image': 'プロフィール画像',
            'account_name': 'アカウント名',
            'gender': '性別',
            'birth_of_date': '生年月日',
            'bio': '自己紹介',
        }
        widgets = {
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'account_name': forms.TextInput(attrs={'placeholder': 'フリー入力'}),
            'gender': forms.Select(choices=[('M', '男性'), ('F', '女性'), ('O', 'その他')]),
            'birth_of_date': forms.SelectDateWidget(years=range(1900, 2024)),
            'bio': forms.Textarea(attrs={'placeholder': 'フリー入力'}),
        }



#欲しいものリスト投稿のフォーム        
class WishlistItemForm(forms.ModelForm):
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
                'placeholder': 'メモを入力してください',
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