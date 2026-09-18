from django.urls import path

from . import views

app_name = 'leads'

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('book-a-call/', views.book_a_call, name='book_a_call'),
]
