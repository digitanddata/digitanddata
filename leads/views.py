from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import BookingForm, ContactForm
from .models import Booking, Lead


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.source_page = request.POST.get('source_page', '/contact/')
            lead.save()
            messages.success(request, "Thanks for reaching out — we'll be in touch soon.")
            return redirect('leads:contact')
    else:
        form = ContactForm()
    return render(request, 'leads/contact.html', {
        'active_nav': 'contact',
        'form': form,
        'breadcrumbs': [('Contact', None)],
    })


def book_a_call(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            lead = Lead.objects.create(
                parent_name=data['parent_name'],
                email=data['email'],
                whatsapp=data['whatsapp'],
                child_subject=data['child_subject'],
                child_curriculum=data['child_curriculum'],
                child_level=data['child_level'],
                message=data['message'],
                source_page='/book-a-call/',
            )
            Booking.objects.create(
                lead=lead,
                requested_time=data['requested_time'],
                timezone=data['timezone'],
            )
            messages.success(
                request, "Your discovery call request has been received — we'll confirm a time shortly."
            )
            return redirect('leads:book_a_call')
    else:
        form = BookingForm()
    return render(request, 'leads/book_a_call.html', {
        'active_nav': None,
        'form': form,
        'breadcrumbs': [('Book a Discovery Call', None)],
    })
