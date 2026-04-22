from django.contrib import admin
from .models import Apartment, Roommate, Rating

@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'monthly_rent', 'bedrooms', 'bathrooms', 'date_added']
    search_fields = ['name', 'address']
    list_filter = ['has_parking', 'is_pet_friendly', 'has_in_unit_laundry']

@admin.register(Roommate)
class RoommateAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at']
    search_fields = ['name', 'email']

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['apartment', 'roommate', 'score', 'rated_at']
    list_filter = ['score']
