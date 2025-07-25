from django.db import models
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os

class Chamado(models.Model):
    class Categoria(models.TextChoices):
        SOFTWARE = 'software', 'Software'
        REDE = 'rede', 'Rede'
        HARDWARE = 'hardware', 'Hardware'
        COMUNICACAO = 'comunicacao', 'Comunicação'
        CONFIGURACOES = 'configuracoes', 'Configurações'
        OUTROS = 'outros', 'Outros'

    class Prioridade(models.TextChoices):
        BAIXA = 'baixa', 'Baixa'
        ALTA = 'alta', 'Alta'
        URGENTE = 'urgente', 'Urgente'

    class Status(models.TextChoices):
        ABERTO = 'aberto', 'Aberto/Disponível'
        EM_ATENDIMENTO = 'em_atendimento', 'Em Atendimento'
        FECHADO = 'fechado', 'Fechado'

    id_protocolo = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100, verbose_name='Título')
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chamados_criados',
        limit_choices_to={'tipo_usuario': 'cliente'},
        verbose_name='Cliente'
    )
    tecnico = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='chamados_assumidos',
        limit_choices_to={'tipo_usuario': 'tecnico'},
        verbose_name='Técnico Responsável'
    )
    descricao = models.TextField(verbose_name='Descrição')
    anexo = models.FileField(upload_to='chamados/anexos/', null=True, blank=True, verbose_name='Anexo')
    categoria = models.CharField(
        max_length=20,
        choices=Categoria.choices,
        default=Categoria.OUTROS,
        verbose_name='Categoria'
    )
    prioridade = models.CharField(
        max_length=10,
        choices=Prioridade.choices,
        default=Prioridade.BAIXA,
        verbose_name='Prioridade'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ABERTO,
        verbose_name='Status'
    )
    tecnico = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True, blank=True,
    related_name='chamados_assumidos',
    limit_choices_to={'tipo_usuario': 'tecnico'},
    verbose_name='Técnico Responsável'
    )
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    data_fechamento = models.DateTimeField(null=True, blank=True, verbose_name='Data de Fechamento')
    solucao = models.TextField(null=True, blank=True, verbose_name='Solução')
    anexo_cliente = models.FileField(upload_to='anexos/', blank=True, null=True)
    anexo_tecnico = models.FileField(upload_to='anexos/', blank=True, null=True)
    anexo_solucao = models.FileField(upload_to='anexos/', blank=True, null=True)

    class Meta:
        db_table = 'chamado'
        verbose_name = "Chamado"
        verbose_name_plural = "Chamados"

    def __str__(self):
        return f"{self.id_protocolo} - {self.titulo}"

    def get_data_criacao(self):
        return self.data_criacao.strftime('%d/%m/%Y %H:%M')

    def get_data_fechamento(self):
        if self.data_fechamento:
            return self.data_fechamento.strftime('%d/%m/%Y %H:%M')
        return '-'

    def get_data_reabertura(self):
        if self.data_reabertura:
            return self.data_reabertura.strftime('%d/%m/%Y %H:%M')
        return '-'
    
    def delete(self, *args, **kwargs):
        if self.anexo and self.anexo.name and os.path.isfile(self.anexo.path):
            os.remove(self.anexo.path)
        if self.anexo_cliente and self.anexo_cliente.name and os.path.isfile(self.anexo_cliente.path):
            os.remove(self.anexo_cliente.path)
        if self.anexo_tecnico and self.anexo_tecnico.name and os.path.isfile(self.anexo_tecnico.path):
            os.remove(self.anexo_tecnico.path)
        if self.anexo_solucao and self.anexo_solucao.name and os.path.isfile(self.anexo_solucao.path):
            os.remove(self.anexo_solucao.path)
        super().delete(*args, **kwargs)
        
@receiver(post_delete, sender=Chamado)
def apagar_arquivos_ao_deletar_chamado(sender, instance, **kwargs):
    for field in ['anexo', 'anexo_cliente', 'anexo_tecnico', 'anexo_solucao']:
        f = getattr(instance, field, None)
        if f and f.name:
            try:
                if os.path.isfile(f.path):
                    os.remove(f.path)
            except Exception:
                pass