from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'property', 'room', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('booking__guest__email', 'comment', 'property__name', 'room__room_number')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)