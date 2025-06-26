from django.db import models

from django.db import models
from django.conf import settings

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
        FECHADO = 'fechado', 'Fechado'
        CONCLUIDO = 'concluido', 'Concluído'
        REABERTO = 'reaberto', 'Reaberto'

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
        max_length=10,
        choices=Status.choices,
        default=Status.ABERTO,
        verbose_name='Status'
    )
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    data_fechamento = models.DateTimeField(null=True, blank=True, verbose_name='Data de Fechamento')
    data_reabertura = models.DateTimeField(null=True, blank=True, verbose_name='Data de Reabertura')
    solucao = models.TextField(null=True, blank=True, verbose_name='Solução')
    anexo_solucao = models.FileField(upload_to='chamados/solucoes/', null=True, blank=True, verbose_name='Anexo da Solução')

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