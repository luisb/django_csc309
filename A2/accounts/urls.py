from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    #path('login/', views.login, name='login'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    #path('register/', views.register, name='register'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/view/', views.profile_view, name='profile-view'),
    path('profile/edit/', views.profile_edit, name='profile-edit'),
]