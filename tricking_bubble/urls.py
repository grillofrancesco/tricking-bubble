from django.urls import path

from .views import *

"""
URL configuration for TrickingSettings project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

urlpatterns = [
    path("", toHome, name="home"),
    path("home/", HomeView.as_view(), name="home"),
    path("login/", AuthenticateView.as_view(), name="login"),
    path("register/", AuthenticateView.as_view(), name="register"),
    path("my_profile/", ProfileView.as_view(), name="profile"),
    path("my_progress/", toProgress, name="progress"),
    path("edit_profile/", Edit_CredentialsView.as_view(), name="edit_profile"),
    path("choose_category/", Choice_CategoryView.as_view(), name="category_choice"),
    path("trick_tree/", Trick_TreeView.as_view(), name="trick_tree"),
    path("logout/", LogoutView.as_view(), name="logout"),
]

handler404 = to404Page
handler403 = to403Page
handler400 = to400Page
