from django.contrib import admin

from task.models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "status", "priority", "create_at", "delete_at")
    search_fields = ("title", "description",)
