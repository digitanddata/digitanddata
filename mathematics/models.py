from django.db import models
from django.urls import reverse


class Curriculum(models.Model):
    """A Mathematics board/syllabus (e.g. IB, Cambridge, AP, CBSE...)."""

    class Category(models.TextChoices):
        INTERNATIONAL = 'international', 'International'
        NATIONAL = 'national', 'National / Regional'
        TEST_PREP = 'test_prep', 'Standardized Test / Competitive'

    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, help_text='Used in the URL, e.g. "ib".')
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
        verbose_name = 'Mathematics Curriculum'
        verbose_name_plural = 'Mathematics Curricula'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('mathematics:board_detail', kwargs={'slug': self.slug})
