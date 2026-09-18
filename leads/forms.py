from django import forms

from .models import Booking, Lead


class ContactForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            'parent_name', 'email', 'whatsapp',
            'child_subject', 'child_curriculum', 'child_level', 'message',
        ]
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['requested_time', 'timezone']
        widgets = {
            'requested_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'
            ),
        }

    # Lead fields, collected on the same form and split out in the view.
    parent_name = forms.CharField(max_length=150, label='Your name')
    email = forms.EmailField(label='Email')
    whatsapp = forms.CharField(max_length=30, required=False, label='WhatsApp number')
    child_subject = forms.ChoiceField(
        choices=[('', '---------')] + Lead.Subject.choices, required=False,
        label="Child's subject",
    )
    child_curriculum = forms.CharField(
        max_length=150, required=False, label="Child's curriculum/board"
    )
    child_level = forms.CharField(max_length=100, required=False, label="Child's level/grade")
    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}), required=False, label='Anything else?'
    )

    field_order = [
        'parent_name', 'email', 'whatsapp',
        'child_subject', 'child_curriculum', 'child_level',
        'requested_time', 'timezone', 'message',
    ]
