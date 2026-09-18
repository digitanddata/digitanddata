from django.db import models


class Lead(models.Model):
    """Every inquiry submitted through /contact/ or /book-a-call/."""

    class Subject(models.TextChoices):
        MATHEMATICS = 'mathematics', 'Mathematics'
        COMPUTER_SCIENCE = 'computer_science', 'Computer Science'
        OTHER = 'other', 'Other / Not sure yet'

    parent_name = models.CharField(max_length=150)
    email = models.EmailField()
    whatsapp = models.CharField(max_length=30, blank=True, verbose_name='WhatsApp number')
    child_subject = models.CharField(
        max_length=20, choices=Subject.choices, blank=True, verbose_name="Child's subject"
    )
    child_curriculum = models.CharField(
        max_length=150, blank=True, verbose_name="Child's curriculum/board"
    )
    child_level = models.CharField(max_length=100, blank=True, verbose_name="Child's level/grade")
    message = models.TextField(blank=True)
    source_page = models.CharField(
        max_length=255, blank=True, help_text='Page the inquiry was submitted from.'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.parent_name} <{self.email}>'


class Booking(models.Model):
    """A discovery-call request linked to a Lead."""

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='bookings')
    requested_time = models.DateTimeField()
    timezone = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-requested_time']

    def __str__(self):
        return f'Booking for {self.lead.parent_name} @ {self.requested_time}'
