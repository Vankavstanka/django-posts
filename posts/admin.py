from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display  = ("id", "title", "userId")
    search_fields = ("title",)
    list_filter   = ("userId",)
