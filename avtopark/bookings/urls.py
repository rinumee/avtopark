from django.urls import path
from . import views

urlpatterns = [
    path('', views.booking_list, name='booking_list'),
    path('create/<int:car_id>/', views.booking_create, name='booking_create'),
    path('<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('<int:booking_id>/cancel/', views.booking_cancel, name='booking_cancel'),
    path('<int:booking_id>/confirm/', views.booking_confirm, name='booking_confirm'),
    path('<int:booking_id>/activate/', views.booking_activate, name='booking_activate'),
    path('<int:booking_id>/complete/', views.booking_complete, name='booking_complete'),
]