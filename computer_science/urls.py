from django.urls import path

from . import views

app_name = 'computer_science'

urlpatterns = [
    path('', views.hub, name='hub'),
    path('<slug:slug>/', views.detail, name='detail'),
]
