from django.contrib import admin

from .models import Curriculum, TechnicalTrack


@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'level_range', 'is_published', 'order')
    list_filter = ('category', 'is_published')
    search_fields = ('name', 'summary')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('order', 'is_published')


@admin.register(TechnicalTrack)
class TechnicalTrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'target_age_range', 'is_published', 'order')
    list_filter = ('is_published',)
    search_fields = ('title', 'summary')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('order', 'is_published')
