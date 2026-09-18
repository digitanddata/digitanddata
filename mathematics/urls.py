from django.urls import path

from . import views

app_name = 'mathematics'

urlpatterns = [
    path('', views.hub, name='hub'),
    path('<slug:slug>/', views.board_detail, name='board_detail'),
]
