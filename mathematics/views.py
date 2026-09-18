from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Curriculum


def hub(request):
    curricula = Curriculum.objects.filter(is_published=True)
    grouped = [
        ('International', 'flaticon-worldwide', curricula.filter(category=Curriculum.Category.INTERNATIONAL)),
        ('National / Regional', 'flaticon-home', curricula.filter(category=Curriculum.Category.NATIONAL)),
        ('Standardized Tests / Competitive', 'flaticon-medal', curricula.filter(category=Curriculum.Category.TEST_PREP)),
    ]
    return render(request, 'mathematics/hub.html', {
        'active_nav': 'mathematics',
        'grouped': grouped,
        'breadcrumbs': [('Mathematics', None)],
    })


def board_detail(request, slug):
    board = get_object_or_404(Curriculum, slug=slug, is_published=True)
    siblings = Curriculum.objects.filter(category=board.category, is_published=True)
    return render(request, 'mathematics/board_detail.html', {
        'active_nav': 'mathematics',
        'board': board,
        'siblings': siblings,
        'breadcrumbs': [('Mathematics', reverse('mathematics:hub')), (board.name, None)],
        'cta_heading': f"Ready to talk about {board.name}?",
    })
