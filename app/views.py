
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from app.forms import SignupForm, LoginForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from .models import UserProfile, WishlistItem, Clothes
from .forms import UserProfileForm, WishlistItemForm, ClothingSearchForm
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView, CreateView, FormView
from django.db.models import Q
from django.views.generic.edit import FormView
from django.views.generic.list import ListView



class PortfolioView(View):
    def get(self, request):
        return render(request, "portfolio.html")

class SignupView(View):
    def get(self, request):
        form = SignupForm() 
        return render(request, "signup.html", context={
            "form": form
        })

    def post(self, request):
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
        form = LoginForm()
        return render(request, "login.html", context={
            "form": form
        })

    def post(self, request):
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
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        return render(request, "profile.html", {"user_profile": user_profile})

class WishlistView(View):
    def get(self, request):
        items = WishlistItem.objects.all()
        print(items)
        return render(request, "wishlist.html", {"items": items})

class ClothesView(View):
    def get(self, request):
        return render(request, "clothes.html")

class LogoutView(View):
    def get(self, request):
        return render(request, "login.html")

class EditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        form = UserProfileForm(instance=user_profile)
        return render(request, "edit_profile.html", {"form": form, "user_profile": user_profile})
    
    
    def post(self, request):
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'プロフィールが更新されました！')
            return redirect("profile")
        else:
            messages.error(request, 'プロフィールの更新に失敗しました。入力内容を確認してください。')
            print(form.errors)
        return render(request, "edit_profile.html", {"form": form, "user_profile": user_profile})



@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'profile': user_profile})

class Wishlist_detailView(View):
    def get(self, request, item_id):
     item = get_object_or_404(WishlistItem, id=item_id)
     return render(request, 'wishlist_detail.html', {'item': item})


class Wishlist_createView(View):
    def get(self, request):
        form = WishlistItemForm()
        return render(request, 'wishlist_create.html', {'form': form})

    def post(self, request):
        form = WishlistItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('wishlist')
        
class WishlistDeleteView(DeleteView):
    model = WishlistItem
    success_url = reverse_lazy('wishlist')
    
    
class Clothes_createView(CreateView):
    model = Clothes
    fields = '__all__'
    template_name = 'clothes_create.html'
    success_url = reverse_lazy('clothes')
    

class ClothingSearchView(FormView):
    template_name = 'clothes.html'
    form_class = ClothingSearchForm
    
    def get_context_data(self, **kwargs):
        # デフォルトのコンテキストを取得
        context = super().get_context_data(**kwargs)

        products = Clothes.objects.all()
        form = self.get_form()
        if form.is_valid():
            gender = form.cleaned_data.get('gender')
            size = form.cleaned_data.get('size')
            color = form.cleaned_data.get('color')
            genre = form.cleaned_data.get('genre')

        if gender:
            products = products.filter(gender__in=gender)
        if size:
            products = products.filter(size__in=size)
        if color:
            products = products.filter(color__in=color)
        if genre:
            products = products.filter(genre__in=genre)

        # フィルタリングされた結果をコンテキストに渡す
        context['products']  = products
        return context