from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from .forms import BlogPostForm
from .models import BlogPost


def _unique_slug(title):
    base = slugify(title)[:190] or 'post'
    slug = base
    suffix = 2
    while BlogPost.objects.filter(slug=slug).exists():
        slug = f'{base}-{suffix}'
        suffix += 1
    return slug


def hub(request):
    posts = BlogPost.objects.filter(is_published=True)
    grouped = [
        ('Mathematics', 'flaticon-notebook', posts.filter(category=BlogPost.Category.MATHEMATICS)),
        ('Computer Science', 'flaticon-monitor', posts.filter(category=BlogPost.Category.COMPUTER_SCIENCE)),
    ]
    return render(request, 'blog/hub.html', {
        'active_nav': 'blog',
        'grouped': grouped,
        'breadcrumbs': [('Blog', None)],
    })


def detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    siblings = BlogPost.objects.filter(category=post.category, is_published=True)
    return render(request, 'blog/post_detail.html', {
        'active_nav': 'blog',
        'post': post,
        'siblings': siblings,
        'breadcrumbs': [('Blog', reverse('blog:hub')), (post.title, None)],
        'cta_heading': 'Ready to turn curiosity into confidence?',
    })


@staff_member_required(login_url='accounts:login')
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.slug = _unique_slug(post.title)
            post.published_at = timezone.now().date()
            author_name = request.user.get_full_name() or request.user.username
            post.author = author_name or post.author
            post.save()
            messages.success(request, f'"{post.title}" has been saved.')
            return redirect(post.get_absolute_url())
    else:
        form = BlogPostForm(initial={'read_time_minutes': 6, 'is_published': True})

    return render(request, 'blog/create_post.html', {
        'active_nav': 'blog',
        'form': form,
        'breadcrumbs': [('Blog', reverse('blog:hub')), ('New Post', None)],
    })
