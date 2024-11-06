from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # ホーム画面のURL
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),  # 欲しいものリスト画面のURL
]