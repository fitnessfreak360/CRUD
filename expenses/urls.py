from django.urls import path
from . import views

urlpatterns = [
    path('', views.expense_list, name='expense_list'),
    path('add/', views.add_expense, name='add_expense'),
    path('edit/<int:pk>/', views.edit_expense, name='edit_expense'),
    path('delete/<int:pk>/', views.delete_expense, name='delete_expense'),
    path('filter/', views.expense_filter, name='expense_filter'),
    path('register/', views.register, name='register'),
    path('guest/edit/<int:index>/', views.edit_guest_expense, name='edit_guest_expense'),
    path('guest/delete/<int:index>/', views.delete_guest_expense, name='delete_guest_expense'),
]
