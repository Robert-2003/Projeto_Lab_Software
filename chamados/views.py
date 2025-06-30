from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from chamados.models import Chamado

@login_required(login_url='/login/')
def chamados_criados(request):
    chamados_abertos = []
    chamados_fechados = []
    if request.user.tipo_usuario == 'cliente':
        chamados_abertos = Chamado.objects.filter(cliente=request.user, status='aberto')
        chamados_fechados = Chamado.objects.filter(cliente=request.user, status='fechado')
    is_cliente = request.user.tipo_usuario == 'cliente'
    contexto = {
        'chamados_abertos': chamados_abertos,
        'chamados_fechados': chamados_fechados,
        'is_cliente': request.user.tipo_usuario == 'cliente',
    }
    return render(request, 'chamados_criados.html', contexto)

@login_required(login_url='/login/')
def criar_chamado(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        categoria = request.POST.get('categoria')
        prioridade = request.POST.get('prioridade')
        anexo = request.FILES.get('anexo')

        chamado = Chamado.objects.create(
            cliente=request.user,
            titulo=titulo,
            descricao=descricao,
            categoria=categoria,
            prioridade=prioridade,
            anexo=anexo,
            status=Chamado.Status.ABERTO
        )
        return redirect('dashboard')
    return render(request, 'criar_chamado.html', {
        'categorias': Chamado.Categoria.choices,
        'prioridades': Chamado.Prioridade.choices,
    })
    
@login_required(login_url='/login/')
def detalhe_chamado(request, id_protocolo):
    chamado = get_object_or_404(Chamado, id_protocolo=id_protocolo)
    is_cliente = request.user == chamado.cliente
    is_tecnico = request.user.tipo_usuario == 'tecnico'
    contexto = {
        'chamado': chamado,
        'is_cliente': is_cliente,
        'is_tecnico': is_tecnico,
        'user': request.user,
    }
    return render(request, 'chamado.html', contexto)

@login_required(login_url='/login/')
def editar_chamado(request, id_protocolo):
    chamado = get_object_or_404(Chamado, id_protocolo=id_protocolo)
    is_cliente = request.user == chamado.cliente
    is_tecnico = request.user == chamado.tecnico

    if is_cliente and chamado.status not in ['aberto', 'em_atendimento']:
        return redirect('detalhe_chamado', id_protocolo=id_protocolo)
    if is_tecnico and chamado.status != 'em_atendimento':
        return redirect('detalhe_chamado', id_protocolo=id_protocolo)
    if not (is_cliente or is_tecnico):
        return redirect('detalhe_chamado', id_protocolo=id_protocolo)

    if request.method == 'POST':
        # Cliente pode editar tudo dele
        if is_cliente:
            chamado.titulo = request.POST.get('titulo')
            chamado.descricao = request.POST.get('descricao')
            chamado.categoria = request.POST.get('categoria')
            chamado.prioridade = request.POST.get('prioridade')
            if request.FILES.get('anexo_cliente'):
                chamado.anexo_cliente = request.FILES['anexo_cliente']
        elif is_tecnico:
            chamado.prioridade = request.POST.get('prioridade')
            chamado.solucao = request.POST.get('solucao')
            if request.FILES.get('anexo_tecnico'):
                chamado.anexo_tecnico = request.FILES['anexo_tecnico']
        chamado.save()
        return redirect('detalhe_chamado', id_protocolo=id_protocolo)

    return render(request, 'editar_chamado.html', {
        'chamado': chamado,
        'is_cliente': is_cliente,
        'is_tecnico': is_tecnico,
    })

@login_required(login_url='/login/')
def fechar_chamado(request, id_protocolo):
    chamado = get_object_or_404(Chamado, id_protocolo=id_protocolo)
    is_cliente = request.user == chamado.cliente
    is_tecnico = request.user == chamado.tecnico

    if request.method == 'POST':
        if is_cliente and chamado.status in ['aberto', 'em_atendimento']:
            chamado.status = 'fechado'
            chamado.solucao = "O cliente fechou este chamado"
            chamado.data_fechamento = timezone.now()
            chamado.save()
        elif is_tecnico and chamado.status == 'em_atendimento':
            chamado.status = 'fechado'
            chamado.data_fechamento = timezone.now()
            chamado.save()
        return redirect('detalhe_chamado', id_protocolo=id_protocolo)
    return redirect('detalhe_chamado', id_protocolo=id_protocolo)

@login_required(login_url='/login/')
def reabrir_chamado(request, id_protocolo):
    chamado = get_object_or_404(Chamado, id_protocolo=id_protocolo, cliente=request.user)
    if request.method == 'POST' and chamado.status == 'fechado':
        antiga_solucao = chamado.solucao or ""
        chamado.status = 'aberto'
        chamado.solucao = f"Usuário reabriu o chamado.\nAntiga solução: {antiga_solucao}"
        chamado.save()
        return redirect('editar_chamado', id_protocolo=id_protocolo)
    return redirect('detalhe_chamado', id_protocolo=id_protocolo)

@login_required(login_url='/login/')
def deletar_chamado(request, id_protocolo):
    chamado = get_object_or_404(Chamado, id_protocolo=id_protocolo, cliente=request.user)
    if request.method == 'POST' and chamado.status == 'fechado':
        chamado.delete()
        return redirect('dashboard')
    return redirect('detalhe_chamado', id_protocolo=id_protocolo)

def remover_anexo_cliente(request, id_protocolo):
    chamado = get_object_or_404(Chamado, id_protocolo=id_protocolo)
    print("Chamado:", chamado)
    print("Usuário:", request.user)
    print("Anexo:", chamado.anexo_cliente)
    if request.method == 'POST' and chamado.anexo_cliente and request.user == chamado.cliente:
        chamado.anexo_cliente.delete(save=False)
        chamado.anexo_cliente = None
        chamado.save()
    return redirect('editar_chamado', id_protocolo=id_protocolo)

@login_required(login_url='/login/')
def remover_anexo_tecnico(request, id_protocolo):
    chamado = get_object_or_404(Chamado, id_protocolo=id_protocolo)
    if request.method == 'POST' and chamado.anexo_tecnico and request.user == chamado.tecnico:
        chamado.anexo_tecnico.delete(save=False)
        chamado.anexo_tecnico = None
        chamado.save()
    return redirect('editar_chamado', id_protocolo=id_protocolo)

@login_required(login_url='/login/')
def remover_anexo_solucao(request, id_protocolo):
    chamado = get_object_or_404(Chamado, id_protocolo=id_protocolo)
    # Aqui, tanto cliente quanto técnico podem remover? Ajuste conforme sua regra.
    if request.method == 'POST' and chamado.anexo_solucao:
        chamado.anexo_solucao.delete(save=False)
        chamado.anexo_solucao = None
        chamado.save()
    return redirect('editar_chamado', id_protocolo=id_protocolo)

@login_required(login_url='/login/')
def lista_chamados(request):
    chamados_disponiveis = Chamado.objects.filter(status='aberto')
    chamados_em_atendimento = Chamado.objects.filter(status='em_atendimento', tecnico=request.user)
    contexto = {
        'chamados_disponiveis': chamados_disponiveis,
        'chamados_em_atendimento': chamados_em_atendimento,
        'is_tecnico': request.user.tipo_usuario == 'tecnico',
        'user': request.user,
    }
    return render(request, 'lista_chamados.html', contexto)

@login_required(login_url='/login/')
def aceitar_chamado(request, id_protocolo):
    chamado = get_object_or_404(Chamado, id_protocolo=id_protocolo, status='aberto')
    if request.method == 'POST' and request.user.tipo_usuario == 'tecnico':
        chamado.status = 'em_atendimento'
        chamado.tecnico = request.user
        chamado.save()
    return redirect('dashboard')

@login_required(login_url='/login/')
def cancelar_chamado(request, id_protocolo):
    chamado = get_object_or_404(Chamado, id_protocolo=id_protocolo)
    if chamado.status != 'em_atendimento' or chamado.tecnico != request.user:
        return redirect('detalhe_chamado', id_protocolo=id_protocolo)
    if request.method == 'POST':
        chamado.status = 'aberto'
        chamado.tecnico = None
        chamado.solucao = ""
        
        if chamado.anexo_tecnico:
            chamado.anexo_tecnico.delete(save=False)
            chamado.anexo_tecnico = None
        
        if hasattr(chamado, 'anexo_solucao') and chamado.anexo_solucao:
            chamado.anexo_solucao.delete(save=False)
            chamado.anexo_solucao = None
        chamado.save()
    return redirect('dashboard')

@login_required(login_url='/login/')
def historico_tecnico(request):
    chamados_fechados = Chamado.objects.filter(tecnico=request.user, status='fechado')
    return render(request, 'historico_tecnico.html', {'chamados_fechados': chamados_fechados})

@login_required(login_url='/login/')
def editar_solucao(request, id_protocolo):
    chamado = get_object_or_404(Chamado, id_protocolo=id_protocolo)
    if request.user != chamado.tecnico:
        return redirect('detalhe_chamado', id_protocolo=id_protocolo)
    if request.method == 'POST':
        chamado.solucao = request.POST.get('solucao')
        if request.FILES.get('anexo_tecnico'):
            chamado.anexo_tecnico = request.FILES['anexo_tecnico']
        chamado.save()
        return redirect('detalhe_chamado', id_protocolo=id_protocolo)
    return render(request, 'editar_solucao.html', {'chamado': chamado})