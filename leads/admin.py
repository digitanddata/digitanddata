from django.contrib import admin

from .models import Booking, Lead


class BookingInline(admin.TabularInline):
    model = Booking
    extra = 0


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        'parent_name', 'email', 'child_subject', 'child_curriculum', 'source_page', 'created_at',
    )
    list_filter = ('child_subject', 'created_at')
    search_fields = ('parent_name', 'email', 'whatsapp', 'message')
    readonly_fields = ('created_at',)
    inlines = [BookingInline]


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('lead', 'requested_time', 'timezone', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('lead__parent_name', 'lead__email')
    readonly_fields = ('created_at',)
