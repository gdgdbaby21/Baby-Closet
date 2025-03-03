"""
URL configuration for babycloset project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path
from app.views import PortfolioView, SignupView, LoginView, HomeView, ProfileView, WishlistView, ClothesView, LogoutView, EditProfileView, Wishlist_detailView , Wishlist_createView, WishlistDeleteView, ClothesView, ClothesCreateView, ClothesDetailView, ClothesDeleteView, SearchResultsView, HashtagSearchView, CreatePostView, PostDetailView, PostDeleteView, LikeView,like_status, CommentView, DeleteCommentView, ClothesOptionsView,ClothesListView, FilterItemsView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PortfolioView.as_view(), name="portfolio"), 
    path('baby-closet/signup/', SignupView.as_view(), name="signup"),
    path('baby-closet/login/', LoginView.as_view(), name="login"),
    path('baby-closet/home/', HomeView.as_view(), name="home"),
    path('baby-closet/profile/', ProfileView.as_view(), name='profile'),
    path('baby-closet/profile/<str:account_name>/', ProfileView.as_view(), name="profile"),
    path('baby-closet/wishlist/', WishlistView.as_view(), name="wishlist"),
    path('baby-closet/logout/', LogoutView.as_view(), name="logout"),
    path('baby-closet/edit-profile/', EditProfileView.as_view(), name='edit_profile'),
    path('baby-closet/wishlist/item/<int:item_id>/', Wishlist_detailView.as_view(), name='wishlist_detail'),
    path('baby-closet/wishlist/create/', Wishlist_createView.as_view(), name='wishlist_create'),
    path('baby-closet/wishlist/<int:pk>/delete/', WishlistDeleteView.as_view(), name='wishlist_delete'),
    path('baby-closet/clothes/create/', ClothesCreateView.as_view(), name='clothes_create'),
    path('baby-closet/clothes/', ClothesView.as_view(), name='clothes'),
    path('baby-closet/clothes/<int:pk>/', ClothesDetailView.as_view(), name='clothes_detail'),
    path('baby-closet/delete/<int:pk>/', ClothesDeleteView.as_view(), name='delete_clothes'),
    path('baby-closet/search-results/', SearchResultsView.as_view(), name='search-results'),
    path('baby-closet/hashtags/search/', HashtagSearchView.as_view(), name='hashtag_search'),
    path('baby-closet/post/new/', CreatePostView.as_view(), name='create_post'),
    path("baby-closet/like/<int:post_id>/", LikeView.as_view(), name="like"), 
    path('baby-closet/like/<int:post_id>/status/', like_status, name='like_status'), 
    path('baby-closet/post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('baby-closet/post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path("baby-closet/post/<int:post_id>/comment/", CommentView.as_view(), name="add_comment"),
    path('baby-closet/delete-comment/<int:comment_id>/', DeleteCommentView.as_view(), name='delete_comment'),
    path('baby-closet/clothes/list/', ClothesListView.as_view(), name='clothes_list'),
    path('baby-closet/api/clothes-options/', ClothesOptionsView.as_view(), name='clothes-options'),
    path('ibaby-closet/tems/filter/', FilterItemsView.as_view(), name='item_filter'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)