from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='accounts/login.html',
            extra_context={'active_nav': None, 'breadcrumbs': [('Log In', None)]},
        ),
        name='login',
    ),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
