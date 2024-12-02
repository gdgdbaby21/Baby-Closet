from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from app.forms import SignupForm, LoginForm
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from .models import UserProfile, WishlistItem, Clothes, Post, Hashtag
from .forms import UserProfileForm, WishlistItemForm, ClothingForm, PostForm
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView, CreateView
from django.views.generic import DetailView, ListView
from django.db.models import Q
from urllib.parse import unquote

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
    login_url = '/login/' 
    redirect_field_name = 'next'

    def get(self, request):
        posts = Post.objects.all()
        return render(request, "home.html", {"posts": posts})

    


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
    
    

class ClothesCreateView(CreateView):
    model = Clothes
    form_class = ClothingForm
    template_name = 'clothes_create.html'
    success_url = reverse_lazy('clothes') 
    
    def form_invalid(self, form):
        print("フォームエラー:", form.errors)
        return super().form_invalid(form)
    
    def post(self, request, *args, **kwargs):
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
    
    
    
class ClothesDeleteView(DeleteView):
    model = Clothes  
    success_url = reverse_lazy('clothes')
    success_message = "%(title)s を削除しました。"
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(self.request, self.success_message % dict(title=self.object.title))
        return super().delete(request, *args, **kwargs)



class SearchResultsView(ListView):
    model = Clothes
    template_name = 'search_results.html'
    context_object_name = 'clothes'

    def get_queryset(self):
        queryset = Clothes.objects.all()


        gender = self.request.GET.get('gender')
        size = self.request.GET.get('size')
        color = self.request.GET.get('color')
        genre = self.request.GET.get('genre')

        
        print(f"検索条件: gender={gender}, size={size}, color={color}, genre={genre}")


        query = Q()
        if gender:
            query |= Q(gender=gender)
        if size:
            query |= Q(size=size)
        if color:
            query |= Q(color=color)
        if genre:
            query |= Q(genre=genre)

        if query:
            queryset = queryset.filter(query)

        print(f"フィルタリング結果: {queryset}")

        return queryset

  
class HashtagSearchView(ListView):
    model = Post
    template_name = 'hashtag_results.html'
    context_object_name = 'posts'
   
    def get_queryset(self):
        
        query_param = self.request.GET.get('q', None)
        if query_param:
            hashtag_name = unquote(query_param).lstrip('#')
        else:
            hashtag_name = self.kwargs.get('hashtag_name')

        print(f"Searching for hashtag: {hashtag_name}")

        hashtag = get_object_or_404(Hashtag, name=hashtag_name)
        return Post.objects.filter(hashtags=hashtag, is_public=True).order_by('-created_at')
    

class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'create_post.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    
class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get_object(self):
        return get_object_or_404(Post, pk=self.kwargs['pk'])
    
    def post(self, request, pk, *args, **kwargs):
        post = self.get_object()
        if request.user == post.user:
            post.delete()
            return redirect('home')
        else:
            return redirect('post_detail', pk=pk)
        
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.user
    
    def post_list(request):
        posts = Post.objects.select_related("user__userprofile").all()
        return render(request, "your_template.html", {"posts": posts})
        