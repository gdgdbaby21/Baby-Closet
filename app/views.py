from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from app.forms import SignupForm, LoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from .models import User, WishlistItem, Clothes, Post, Hashtag, Like, Comment
from .forms import  UserProfileForm, WishlistItemForm, ClothingForm, PostForm
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView, CreateView
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.db.models import Q, Count
from urllib.parse import unquote
from django.http import JsonResponse, Http404
from django.views.generic.list import ListView
import json, logging
from .utils import extract_hashtags, save_hashtags_to_post



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
        return render(request, "login.html", {"form": LoginForm()})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request, 
                email=form.cleaned_data["email"], 
                password=form.cleaned_data["password"]
            )
            if user:
                login(request, user)
                return redirect(request.GET.get("next", "home"))
        return render(request, "login.html", {"form": form})



class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect("login")


class HomeView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'
    login_url = "/login/"

    def get_queryset(self):
        """非公開投稿のフィルタリング"""
        user = self.request.user
        if user.is_authenticated:
            
            return Post.objects.filter(Q(is_public=True) | Q(user=user)).distinct()
        else:
            return Post.objects.filter(is_public=True).distinct() 

    def get_context_data(self, **kwargs):
        """人気のハッシュタグとその投稿を取得"""
        context = super().get_context_data(**kwargs)

        popular_hashtags = Hashtag.objects.annotate(
            post_count=Count('posts')
        ).order_by('-popularity', '-post_count')[:3]

        hashtag_posts = {
            hashtag: hashtag.posts.filter(Q(is_public=True) | Q(user=self.request.user))[:5]
            for hashtag in popular_hashtags
        }

        context['popular_hashtags'] = popular_hashtags
        context['hashtag_posts'] = hashtag_posts
        return context
    

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request, account_name=None):
        if account_name is None:
            return redirect('profile', account_name=request.user.account_name)

        profile_user = get_object_or_404(User, account_name=account_name)

        if request.user == profile_user:
            user_posts = Post.objects.filter(user=profile_user).order_by('-created_at')
        else:
            user_posts = Post.objects.filter(user=profile_user, is_public=True).order_by('-created_at')

        return render(request, "profile.html", {
            "user_profile": profile_user,
            "user_posts": user_posts,
        })



class WishlistView(LoginRequiredMixin, View):
    def get(self, request):
        items = WishlistItem.objects.filter(user=request.user)  
        return render(request, "wishlist.html", {"items": items})



class ClothesView(LoginRequiredMixin, View):
    def get(self, request):
        clothes = Clothes.objects.filter(user=request.user)
        return render(request, "clothes.html", {"clothes": clothes})



class EditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user_profile = request.user
        form = UserProfileForm(instance=request.user)
        return render(request, "edit_profile.html", {"form": form, "user_profile": user_profile})

    def post(self, request):
        user_profile = request.user
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save() 
            messages.success(request, 'プロフィールが更新されました！')
            return redirect("profile")
        else:
            messages.error(request, 'プロフィールの更新に失敗しました。入力内容を確認してください。')
        return render(request, "edit_profile.html", {"form": form, "user_profile": user_profile})

@login_required
def profile(request):
    user_profile = request.user
    return render(request, 'profile.html', {'profile': user_profile})


class Wishlist_detailView(View):
    def get(self, request, item_id):
     item = get_object_or_404(WishlistItem, id=item_id)
     return render(request, 'wishlist_detail.html', {'item': item})



class Wishlist_createView(LoginRequiredMixin, View):
    def get(self, request):
        form = WishlistItemForm()
        return render(request, 'wishlist_create.html', {'form': form})

    def post(self, request):
        form = WishlistItemForm(request.POST, request.FILES)
        if form.is_valid():
            wishlist_item = form.save(commit=False)
            wishlist_item.user = request.user
            wishlist_item.save()
            return redirect('wishlist')
        return render(request, 'wishlist_create.html', {'form': form})
        
class WishlistDeleteView(DeleteView):
    model = WishlistItem
    success_url = reverse_lazy('wishlist')
    
    
    
class ClothesCreateView(LoginRequiredMixin, CreateView):
    model = Clothes
    form_class = ClothingForm
    template_name = 'clothes_create.html'
    success_url = reverse_lazy('clothes')

    def form_valid(self, form):
        
        clothes = form.save(commit=False)
        clothes.user = self.request.user
        clothes.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print("フォームエラー:", form.errors)
        return super().form_invalid(form)

    def post(self, request, *args, **kwargs):
        print("POSTデータ:", request.POST) 
        print("FILESデータ:", request.FILES)
        return super().post(request, *args, **kwargs)


class ClothesDetailView(DetailView):
    model = Clothes
    template_name = 'clothes_detail.html'
    context_object_name = 'clothes'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_posts'] = self.object.get_related_posts()
        return context



    
class ClothesDeleteView(DeleteView):
    model = Clothes  
    success_url = reverse_lazy('clothes')
    success_message = "%(title)s を削除しました。"
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(self.request, self.success_message % dict(title=self.object.title))
        return super().delete(request, *args, **kwargs)
    
    
class ClothesOptionsView(View):
    def get(self, request):#requestは現在未使用
        genres = Clothes.objects.values_list('genre', flat=True).distinct()
        colors = Clothes.objects.values_list('color', flat=True).distinct()
        sizes = Clothes.objects.values_list('size', flat=True).distinct()

        return JsonResponse({
            'genres': list(genres),
            'colors': list(colors),
            'sizes': list(sizes),
        })


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
    
    
logger = logging.getLogger(__name__)

class HashtagSearchView(ListView):
    model = Post
    template_name = 'hashtag_results.html'
    context_object_name = 'posts'
   
    def get_queryset(self):
        hashtag_name = self.request.GET.get('q') or self.kwargs.get('hashtag_name')
        if not hashtag_name:
            raise Http404("Hashtag not provided.")
        
        hashtag_name = hashtag_name.lstrip('#')

        logger.info(f"Searching for hashtag: {hashtag_name}")

        hashtag = get_object_or_404(Hashtag, name=hashtag_name)
        return Post.objects.filter(hashtags=hashtag).select_related('user').prefetch_related('comments').order_by("-created_at")
    
    


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'create_post.html'
    form_class = PostForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        print("POSTデータ:", self.request.POST)
        print("フォームのクリーンデータ:", form.cleaned_data)
        
        post = form.save(commit=False)
        post.user = self.request.user
        
        post.is_public = self.request.POST.get('is_public') == "1"

        print("保存前の is_public 値:", post.is_public)
        post.save()
        form.save_m2m() 
        
        hashtags = extract_hashtags(post.caption)
        save_hashtags_to_post(post, hashtags)

        
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Clothes.GENRE_CHOICES
        context['colors'] = Clothes.COLOR_CHOICES
        context['sizes'] = Clothes.SIZE_CHOICES
        return context



class FilterItemsView(ListView):
    model = Clothes
    template_name = 'filtered_items.html'
    context_object_name = 'items'

    def get_queryset(self):
        user = self.request.user
        
        genre = self.request.GET.get('genre')
        color = self.request.GET.get('color')
        size = self.request.GET.get('size')

        queryset = Clothes.objects.filter(user=user)

        if genre:
            queryset = queryset.filter(genre=genre)
        if color:
            queryset = queryset.filter(color=color)
        if size:
            queryset = queryset.filter(size=size)

        return queryset



class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        # 投稿者でない場合、非公開の投稿は表示させない
        if not post.is_public and post.user != self.request.user:
            raise Http404("この投稿は非公開です。")
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = self.object.user  # self.get_object() ではなく self.object を使う
        return context
    


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
    

class LikeView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
        
        return JsonResponse({
            "liked": liked,
            "like_count": post.likes.count() 
        })


class CommentView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        data = json.loads(request.body) 
        content = data.get("content")

        if content:
            comment = Comment.objects.create(user=request.user, post=post, content=content)
            return JsonResponse({
                "comment_id": comment.id,
                "user_account": comment.user.account_name,
                "content": comment.content,
                "created_at": comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        return JsonResponse({"error": "コメント内容が空です。"}, status=400)
    
    
class DeleteCommentView(LoginRequiredMixin, View):
    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id, user=request.user)
        comment.delete()
        return JsonResponse({"message": "コメントが削除されました。"})
    


class ClothesOptionsView(TemplateView):
    def get(self, request, *args, **kwargs):
        return JsonResponse({
            'genres': Clothes.GENRE_CHOICES,
            'sizes': Clothes.SIZE_CHOICES,
            'colors': Clothes.COLOR_CHOICES,
        })
    

class ClothesListView(View):
    def get(self, request, *args, **kwargs):
        clothes = Clothes.objects.all()
        data = [
            {
                'id': item.id,
                'title': item.title,
                'genre': item.get_genre_display(),
                'size': item.size,
                'color': item.get_color_display(),
                'image': item.image.url if item.image else None,
            }
            for item in clothes
        ]
        return JsonResponse({'clothes': data})
    
