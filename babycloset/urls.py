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
from app.views import PortfolioView, SignupView, LoginView, HomeView, ProfileView, WishlistView, ClothesView, LogoutView, Edit_profileView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PortfolioView.as_view(), name="portfolio"), 
    path('signup/', SignupView.as_view(), name="signup"),
    path('login/', LoginView.as_view(), name="login"),
    path('home/', HomeView.as_view(), name="home"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('wishlist/', WishlistView.as_view(), name="wishlist"),
    path('clothes/', ClothesView.as_view(), name="clothes"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('edit-profile/', Edit_profileView.as_view(), name='edit_profile'),

]
