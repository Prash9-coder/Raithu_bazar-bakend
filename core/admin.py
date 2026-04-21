from django.contrib import admin
from .models import User, CowListing, CowImage, Inquiry, Favorite

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'role', 'mobile_number', 'district')
    list_filter = ('role', 'state', 'district')

@admin.register(CowListing)
class CowListingAdmin(admin.ModelAdmin):
    list_display = ('tag_name', 'breed', 'seller', 'price', 'status', 'created_at')
    list_filter = ('status', 'breed', 'state')
    search_fields = ('tag_name', 'breed', 'seller__full_name')

@admin.register(CowImage)
class CowImageAdmin(admin.ModelAdmin):
    list_display = ('cow', 'created_at')

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile_number', 'cow', 'created_at')

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'cow', 'created_at')
