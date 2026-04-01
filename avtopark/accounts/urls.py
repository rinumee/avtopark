from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('user/', views.user_dashboard, name='user_dashboard'),
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/users/', views.admin_user_list, name='admin_user_list'),
    path('admin/users/create/', views.admin_user_create, name='admin_user_create'),
    path('admin/users/<int:user_id>/edit/', views.admin_user_edit, name='admin_user_edit'),
    path('admin/users/<int:user_id>/delete/', views.admin_user_delete, name='admin_user_delete'),
    path('admin/settings/', views.admin_settings, name='admin_settings'),
    path('admin/profile/edit/', views.admin_profile_edit, name='admin_profile_edit'),
    path('admin/change-password/', views.admin_change_password, name='admin_change_password'),
    path('logout/', views.logout_view, name='logout'),
]