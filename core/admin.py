from django.contrib import admin

from .models import Testimonial


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'curriculum_tag', 'location', 'rating', 'is_published', 'order')
    list_filter = ('subject', 'rating', 'is_published')
    search_fields = ('name', 'quote', 'curriculum_tag', 'location')
    list_editable = ('order', 'is_published')
