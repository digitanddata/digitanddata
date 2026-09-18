from django.db import models


class Testimonial(models.Model):
    """A parent/student testimonial shown on the /testimonials/ page."""

    class Subject(models.TextChoices):
        MATHEMATICS = 'mathematics', 'Mathematics'
        COMPUTER_SCIENCE = 'computer_science', 'Computer Science'

    name = models.CharField(max_length=150, help_text='Parent or student name (or initials).')
    subject = models.CharField(max_length=20, choices=Subject.choices, default=Subject.MATHEMATICS)
    quote = models.TextField()
    curriculum_tag = models.CharField(
        max_length=100, blank=True, help_text='e.g. "IB Math AA" or "AP Computer Science A".'
    )
    location = models.CharField(max_length=100, blank=True, help_text='e.g. "Singapore" or "London, UK".')
    rating = models.PositiveSmallIntegerField(default=5, help_text='Star rating out of 5.')
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers sort first.')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return f'{self.name} — {self.curriculum_tag or "General"}'
