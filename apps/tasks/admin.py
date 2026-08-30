from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'task_type', 'status', 'assigned_to', 'due_date', 'booking', 'room')
    list_filter = ('task_type', 'status', 'due_date', 'assigned_to')
    search_fields = ('title', 'description', 'assigned_to__email', 'booking__id', 'room__room_number')
    readonly_fields = ('created_at', 'updated_at', 'completed_at')
    ordering = ('-created_at',)