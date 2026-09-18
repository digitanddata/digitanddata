from django import forms

from .models import BlogPost


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'category', 'excerpt', 'body', 'read_time_minutes', 'is_published']
        widgets = {
            'excerpt': forms.Textarea(attrs={'rows': 2}),
            'body': forms.Textarea(attrs={'rows': 16}),
        }
        labels = {
            'is_published': 'Publish immediately (uncheck to save as a draft)',
        }
