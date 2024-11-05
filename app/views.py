from django.shortcuts import render, redirect
from django.views import View
from app.forms import SignupForm, LoginForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
#プロフィール編集画面用
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm





class PortfolioView(View):
    def get(self, request):
        return render(request, "portfolio.html")

class SignupView(View):
    def get(self, request):
        form = SignupForm() 
        return render(request, "signup.html", context={
            "form":form
        })
    def post(self, request):
        print(request.POST)
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        return render(request, "signup.html", context={
            "form": form
        })

class LoginView(View):
    def get(self, request):
        return render(request, "login.html")
    def post(self, request):
        print(request.POST)
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect("home")
        return render(request, "login.html", context={
            "form": form
        })
    
       
class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "home.html")

    
class ProfileView(View):
    def get(self, request):
        return render(request, "profile.html")

    
class WishlistView(View):
    def get(self, request):
        return render(request, "wishlist.html")


class ClothesView(View):
    def get(self, request):
        return render(request, "clothes.html")
    

class LogoutView(View):
    def get(self, request):
        return render(request, "login.html")
    
    
class Edit_profileView(LoginRequiredMixin, View):
    def get(self, request):
        user_profile, created = UserProfile.objects.get_or_create(ユーザー=request.user)
        form = UserProfileForm(instance=user_profile)
        return render(request, "edit_profile.html", {"from": form})
    
    
    def post(self, request):
        user_profile, created = UserProfile.objects.get_or_create(ユーザー=request.user)
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect("profile")  # プロフィール表示ページにリダイレクト
        return render(request, "edit_profile.html", {"form": form})
    
    
    
@login_required
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(ユーザー=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  #プロフィール表示ページにリダイレクト
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'edit_profile.html', {'form': form})


@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(ユーザー=request.user)
    return render(request, 'profile.html', {'profile': user_profile})

