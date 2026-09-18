from django.shortcuts import render

from .models import Testimonial


def home(request):
    featured_testimonials = Testimonial.objects.filter(is_published=True)[:6]
    return render(request, 'core/home.html', {
        'active_nav': 'home',
        'featured_testimonials': featured_testimonials,
    })


def about(request):
    return render(request, 'core/about.html', {
        'active_nav': 'about',
        'breadcrumbs': [('About Us', None)],
    })


def pricing(request):
    return render(request, 'core/pricing.html', {
        'active_nav': 'pricing',
        'breadcrumbs': [('Pricing', None)],
    })


def testimonials(request):
    items = Testimonial.objects.filter(is_published=True)
    grouped = [
        ('Mathematics', 'mathematics', items.filter(subject=Testimonial.Subject.MATHEMATICS)),
        ('Computer Science', 'computer_science', items.filter(subject=Testimonial.Subject.COMPUTER_SCIENCE)),
    ]
    return render(request, 'core/testimonials.html', {
        'active_nav': 'testimonials',
        'grouped': grouped,
        'breadcrumbs': [('Testimonials', None)],
    })
