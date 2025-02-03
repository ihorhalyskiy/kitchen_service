from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import UserLoginForm
from django.contrib.auth.models import User

def home(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('kitchen:dashboard')
            else:
                messages.error(request, "Invalid credentials. Please register.")
                return redirect('kitchen:register')
        else:
            messages.error(request, "Form is not valid. Please try again.")
    else:
        form = UserLoginForm()
    return render(request, 'kitchen/home.html', {'form': form})

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password=password)
                user.save()
                return redirect('home')
            else:
                return render(request, 'kitchen/register.html', {'error': 'Username already exists'})
    return render(request, 'kitchen/register.html')

def dashboard(request):
    return render(request, 'kitchen/dashboard.html')

