from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from usuarios.models import Usuario
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import date
from django.http.response import Http404, JsonResponse
from django.core.mail import send_mail

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

@login_required(login_url='/login/')
def dashboard(request):
    usuario = request.user
    usuarios = Usuario.objects.all()
    contexto = {
        'usuario': usuario,
        'usuarios': usuarios,
        'is_admin': usuario.is_superuser,
    }
    return render(request, 'dashboard.html', contexto)

@login_required(login_url='/login/')
def novo_usuario(request):
    if request.method == 'POST':
        matricula = request.POST.get('matricula')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        tipo_usuario = request.POST.get('tipo_usuario')

        if not matricula or not username or not password or not tipo_usuario or not email:
            messages.error(request, "Preencha todos os campos obrigatórios.")
            return redirect('novo_usuario')

        if Usuario.objects.filter(matricula=matricula).exists():
            messages.error(request, "Já existe um usuário com essa matrícula.")
            return redirect('novo_usuario')

        if Usuario.objects.filter(username=username).exists():
            messages.error(request, "Já existe um usuário com esse username.")
            return redirect('novo_usuario')

        usuario = Usuario(
            matricula=matricula,
            username=username,
            email=email,
            tipo_usuario=tipo_usuario
        )
        usuario.set_password(password)
        usuario.save()

        messages.success(request, f"Usuário criado com matrícula {usuario.matricula}")
        return redirect('dashboard')
    
    usernames = list(Usuario.objects.values_list('username', flat=True))
    return render(request, 'novo_usuario.html', {'usernames': usernames})