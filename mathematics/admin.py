from django.contrib import admin

from .models import Curriculum


@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'level_range', 'is_published', 'order')
    list_filter = ('category', 'is_published')
    search_fields = ('name', 'summary')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('order', 'is_published')
