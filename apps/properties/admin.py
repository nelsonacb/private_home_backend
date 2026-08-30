from django.contrib import admin
from .models import Property, Room

class RoomInline(admin.TabularInline):
    model = Room
    extra = 1
    fields = ('room_number', 'room_type', 'capacity', 'price_per_night', 'is_available')

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'price_per_night', 'owner', 'is_active', 'max_guests')
    list_filter = ('city', 'province', 'is_active', 'owner')
    search_fields = ('name', 'address', 'owner__email')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [RoomInline]

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'property', 'room_type', 'capacity', 'price_per_night', 'is_available')
    list_filter = ('room_type', 'is_available', 'property')
    search_fields = ('room_number', 'property__name')
    readonly_fields = ('created_at', 'updated_at')