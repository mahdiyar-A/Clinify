from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect('index')
        return render(request, 'core/login.html', {'error': 'Invalid credentials'})
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    return render(request, 'core/register.html')

@login_required
def patient_dashboard(request):
    return render(request, 'core/patient_dashboard.html')

@login_required
def doctor_dashboard(request):
    return render(request, 'core/doctor_dashboard.html')

@login_required
def admin_dashboard(request):
    return render(request, 'core/admin_dashboard.html')