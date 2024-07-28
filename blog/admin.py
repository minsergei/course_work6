from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "heading_blog",
        "content_blog",
    )
