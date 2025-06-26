from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from usuarios.models import Usuario
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import date
from django.http.response import Http404, JsonResponse

def login_user(request):
    return render(request, 'login.html')
def logout_user(request):
    logout(request)
    return redirect('/')

def submit_login(request):
    if request.POST:
        matricula = request.POST.get('matricula')
        senha = request.POST.get('senha')
        usuario = authenticate(request, matricula=matricula, password=senha)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, "Matrícula ou senha inválido")
    return redirect('/')