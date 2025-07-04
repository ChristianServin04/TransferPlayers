from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html')

def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    return render(request, 'register.html')

def admin_view(request):
    return render(request, 'admin_panel.html')

def player_view(request):
    return render(request, 'player.html')