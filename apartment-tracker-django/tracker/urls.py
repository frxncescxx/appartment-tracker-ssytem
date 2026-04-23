from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('apartments/', views.apartments, name='apartments'),
    path('apartments/<int:pk>/edit/', views.apartment_edit, name='apartment_edit'),
    path('apartments/<int:pk>/delete/', views.apartment_delete, name='apartment_delete'),
    path('roommates/', views.roommates, name='roommates'),
    path('roommates/<int:pk>/edit/', views.roommate_edit, name='roommate_edit'),
    path('roommates/<int:pk>/delete/', views.roommate_delete, name='roommate_delete'),
    path('rate/', views.rate, name='rate'),
    path('compare/', views.compare, name='compare'),
]
