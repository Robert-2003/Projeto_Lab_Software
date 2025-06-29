from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from usuarios.models import Usuario
from chamados.models import Chamado
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
    usuarios_adm = Usuario.objects.filter(tipo_usuario='adm')
    usuarios_tecnico = Usuario.objects.filter(tipo_usuario='tecnico')
    usuarios_cliente = Usuario.objects.filter(tipo_usuario='cliente')
    is_cliente = request.user.tipo_usuario == 'cliente'
    
    chamados_disponiveis = []
    chamados_em_atendimento = []
    if request.user.tipo_usuario == 'tecnico':
        chamados_disponiveis = Chamado.objects.filter(status='aberto')
        chamados_em_atendimento = Chamado.objects.filter(status='em_atendimento', tecnico=request.user)
    
    chamados_abertos = []
    chamados_fechados = []
    if request.user.tipo_usuario == 'cliente':
        chamados_abertos = Chamado.objects.filter(cliente=request.user, status='aberto')
        chamados_em_atendimento = Chamado.objects.filter(cliente=request.user, status='em_atendimento')
        chamados_fechados = Chamado.objects.filter(cliente=request.user, status='fechado')
    
    contexto = {
        'usuarios_adm': usuarios_adm,
        'usuarios_tecnico': usuarios_tecnico,
        'usuarios_cliente': usuarios_cliente,
        'is_cliente': is_cliente,
        'is_admin': request.user.is_superuser,
        
        'chamados_disponiveis': chamados_disponiveis,
        'chamados_em_atendimento': chamados_em_atendimento,
        'is_tecnico': request.user.tipo_usuario == 'tecnico',
        
        'chamados_abertos': chamados_abertos,
        'chamados_fechados': chamados_fechados,
        'is_cliente': request.user.tipo_usuario == 'cliente',
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

@login_required(login_url='/login/')
def usuario(request, matricula):
    try:
        usuario_obj = Usuario.objects.get(matricula=matricula)
    except Usuario.DoesNotExist:
        raise Http404("Usuário não encontrado")
    contexto = {
        'usuario': usuario_obj,
        'is_admin': request.user.is_superuser,
    }
    return render(request, 'usuario.html', contexto)

@login_required(login_url='/login/')
def editar_usuario(request, matricula):
    usuario = get_object_or_404(Usuario, matricula=matricula)
    if request.method == 'POST':
        usuario.username = request.POST.get('username')
        usuario.email = request.POST.get('email')
        usuario.tipo_usuario = request.POST.get('tipo_usuario')
        usuario.save()
        messages.success(request, "Usuário atualizado com sucesso!")
        return redirect('usuario', matricula=usuario.matricula)
    return render(request, 'editar_usuario.html', {'usuario': usuario})

@login_required(login_url='/login/')
def deletar_usuario(request, matricula):
    usuario = get_object_or_404(Usuario, matricula=matricula)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, "Usuário deletado com sucesso!")
        return redirect('dashboard')
    return render(request, 'usuario.html', {'usuario': usuario})

@login_required(login_url='/login/')
def dashboard_tecnico(request):
    chamados_disponiveis = Chamado.objects.filter(status='aberto')
    chamados_assumidos = Chamado.objects.filter(status='em_atendimento', tecnico=request.user)
    return render(request, 'dashboard_tecnico.html', {
        'chamados_disponiveis': chamados_disponiveis,
        'chamados_assumidos': chamados_assumidos,
    })

@login_required(login_url='/login/')
def aceitar_chamado(request, id_protocolo):
    chamado = get_object_or_404(Chamado, id_protocolo=id_protocolo, status='aberto')
    if request.method == 'POST':
        chamado.status = 'em_atendimento'
        chamado.tecnico = request.user
        chamado.save()
    return redirect('dashboard_tecnico')

@login_required(login_url='/login/')
def cancelar_chamado(request, id_protocolo):
    chamado = get_object_or_404(Chamado, id_protocolo=id_protocolo, status='em_atendimento', tecnico=request.user)
    if request.method == 'POST':
        chamado.status = 'aberto'
        chamado.tecnico = None
        chamado.save()
    return redirect('dashboard_tecnico')

@login_required(login_url='/login/')
def fechar_chamado(request, id_protocolo):
    chamado = get_object_or_404(Chamado, id_protocolo=id_protocolo, status='em_atendimento', tecnico=request.user)
    if request.method == 'POST':
        chamado.status = 'fechado'
        chamado.save()
    return redirect('dashboard_tecnico')