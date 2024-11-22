
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from app.forms import SignupForm, LoginForm
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from .models import UserProfile, WishlistItem, Clothes
from .forms import UserProfileForm, WishlistItemForm, ClothingForm
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView, CreateView
from django.views.generic import DetailView


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
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


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
    
    

class ClothingSearchView(View):
    def get(self, request):
        # クエリパラメータから条件を取得
        gender = request.GET.getlist('gender')
        size = request.GET.getlist('size')
        color = request.GET.getlist('color')
        genre = request.GET.getlist('genre')

        # データをフィルタリング
        clothes = Clothes.objects.all()
        if gender:
            clothes = clothes.filter(gender__in=gender)
        if size:
            clothes = clothes.filter(size__in=size)
        if color:
            clothes = clothes.filter(color__in=color)
        if genre:
            clothes = clothes.filter(genre__in=genre)

        # データをテンプレートに渡す
        return render(request, 'clothes.html', {'clothes': clothes})
    
    
class ClothesCreateView(CreateView):
    model = Clothes
    form_class = ClothingForm
    template_name = 'clothes_create.html'
    success_url = reverse_lazy('clothes') 
    
    def form_invalid(self, form):
        print("フォームエラー:", form.errors)
        return super().form_invalid(form)
    
    def post(self, request, *args, **kwargs):
        # デバッグ用: アップロードされたデータを確認
        print("POSTデータ:", request.POST)
        print("FILESデータ:", request.FILES)
        return super().post(request, *args, **kwargs)
    

class ClothesView(View):
    def get(self, request):
        clothes = Clothes.objects.all()

        return render(request, "clothes.html", {"clothes": clothes})


class ClothesDetailView(DetailView):
    model = Clothes
    template_name = 'clothes_detail.html'
    context_object_name = 'item'
    

        
    