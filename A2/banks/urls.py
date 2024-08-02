from django.urls import path

from . import views

urlpatterns = [
    path('all/', views.BankListView.as_view(), name='bank-list'),
    path('add/', views.BankCreateView.as_view(), name='bank-add'),
    path('<int:pk>/details/', views.BankDetailView.as_view(), name='bank-detail'),
    
    path('<int:pk>/branches/', views.BranchListView.as_view(), name='branch-list'),
    path('<int:pk>/branches/add/', views.BranchCreateView.as_view(), name='branch-add'),
    path('branch/<int:pk>/details/', views.BranchDetailView.as_view(), name='branch-detail'),
]
