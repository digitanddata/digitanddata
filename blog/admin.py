from django.contrib import admin

from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'published_at', 'read_time_minutes', 'is_published')
    list_filter = ('category', 'is_published')
    search_fields = ('title', 'excerpt', 'body')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_published',)
    date_hierarchy = 'published_at'
