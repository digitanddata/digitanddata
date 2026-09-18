from django.db import models
from django.urls import reverse


class Curriculum(models.Model):
    """A Computer Science school board/syllabus (e.g. IB CS, AP CS A...)."""

    class Category(models.TextChoices):
        INTERNATIONAL = 'international', 'International'
        NATIONAL = 'national', 'National / Regional'

    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, help_text='Used in the URL, e.g. "ap-cs-a".')
    category = models.CharField(max_length=20, choices=Category.choices)
    level_range = models.CharField(
        max_length=100, blank=True, help_text='e.g. "Grades 6-12" or "Ages 11-18".'
    )
    summary = models.TextField(blank=True, help_text='Short description shown on the hub page.')
    syllabus_outline = models.TextField(
        blank=True, help_text='Longer outline shown on the board detail page.'
    )
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers sort first.')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'order', 'name']
        verbose_name = 'Computer Science Curriculum'
        verbose_name_plural = 'Computer Science Curricula'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('computer_science:detail', kwargs={'slug': self.slug})


class TechnicalTrack(models.Model):
    """A technical-skills track beyond the school syllabus (e.g. Robotics)."""

    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, help_text='Used in the URL, e.g. "robotics".')
    summary = models.TextField(blank=True, help_text='Short description shown on the hub page.')
    syllabus_outline = models.TextField(
        blank=True, help_text='Longer outline shown on the track detail page.'
    )
    target_age_range = models.CharField(
        max_length=100, blank=True, help_text='e.g. "Ages 10-16".'
    )
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers sort first.')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = 'Technical Track'
        verbose_name_plural = 'Technical Tracks'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('computer_science:detail', kwargs={'slug': self.slug})
