from django.db import models
from django.urls import reverse
from django.utils import timezone


class BlogPost(models.Model):
    """An article on the DigitAndData blog, covering Mathematics or Computer Science."""

    class Category(models.TextChoices):
        MATHEMATICS = 'mathematics', 'Mathematics'
        COMPUTER_SCIENCE = 'computer_science', 'Computer Science'

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, help_text='Used in the URL, e.g. "why-primes-refuse-to-behave".')
    category = models.CharField(max_length=20, choices=Category.choices)
    excerpt = models.TextField(help_text='Short teaser shown on the blog grid.')
    body = models.TextField(help_text='Full article body, shown on the article detail page.')
    author = models.CharField(max_length=100, default='DigitAndData Team')
    read_time_minutes = models.PositiveIntegerField(default=6, help_text='Approximate reading time in minutes.')
    published_at = models.DateField(default=timezone.now)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})
