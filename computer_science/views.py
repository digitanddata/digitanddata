from django.http import Http404
from django.shortcuts import render
from django.urls import reverse

from .models import Curriculum, TechnicalTrack


def hub(request):
    curricula = Curriculum.objects.filter(is_published=True)
    grouped = [
        ('International', 'flaticon-worldwide', curricula.filter(category=Curriculum.Category.INTERNATIONAL)),
        ('National / Regional', 'flaticon-home', curricula.filter(category=Curriculum.Category.NATIONAL)),
    ]
    tracks = TechnicalTrack.objects.filter(is_published=True)
    return render(request, 'computer_science/hub.html', {
        'active_nav': 'computer_science',
        'grouped': grouped,
        'tracks': tracks,
        'breadcrumbs': [('Computer Science', None)],
    })


def detail(request, slug):
    """Serves both school-curriculum board pages and technical track pages
    under the same /computer-science/<slug>/ URL shape (see README sitemap).
    """
    board = Curriculum.objects.filter(slug=slug, is_published=True).first()
    if board is not None:
        siblings = Curriculum.objects.filter(category=board.category, is_published=True)
        return render(request, 'computer_science/board_detail.html', {
            'active_nav': 'computer_science',
            'board': board,
            'siblings': siblings,
            'breadcrumbs': [('Computer Science', reverse('computer_science:hub')), (board.name, None)],
            'cta_heading': f"Ready to talk about {board.name}?",
        })

    track = TechnicalTrack.objects.filter(slug=slug, is_published=True).first()
    if track is not None:
        siblings = TechnicalTrack.objects.filter(is_published=True)
        return render(request, 'computer_science/track_detail.html', {
            'active_nav': 'computer_science',
            'track': track,
            'siblings': siblings,
            'breadcrumbs': [('Computer Science', reverse('computer_science:hub')), (track.title, None)],
            'cta_heading': f"Ready to talk about {track.title}?",
        })

    raise Http404('No curriculum board or technical track matches this slug.')
