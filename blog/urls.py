from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.hub, name='hub'),
    path('new/', views.create_post, name='create_post'),
    path('<slug:slug>/', views.detail, name='detail'),
]
