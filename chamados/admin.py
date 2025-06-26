from django.contrib import admin
from .models import Chamado

@admin.register(Chamado)
class ChamadoAdmin(admin.ModelAdmin):
    list_display = (
        'id_protocolo', 'titulo', 'cliente', 'tecnico', 'categoria',
        'prioridade', 'status', 'data_criacao', 'data_fechamento'
    )
    search_fields = ('id_protocolo', 'titulo', 'cliente__matricula', 'tecnico__matricula')
    list_filter = ('categoria', 'prioridade', 'status', 'data_criacao', 'data_fechamento')
    ordering = ('-data_criacao',)