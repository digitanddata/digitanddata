from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import StudentSignupForm


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}! Your student account is ready.')
            return redirect('home')
    else:
        form = StudentSignupForm()

    return render(request, 'accounts/signup.html', {
        'active_nav': None,
        'form': form,
        'breadcrumbs': [('Sign Up', None)],
    })
