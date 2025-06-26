from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'username', 'first_name', 'last_name', 'tipo_usuario', 'data_cadastro')
    search_fields = ('matricula', 'username', 'first_name', 'last_name')
    list_filter = ('tipo_usuario', 'data_cadastro')
    ordering = ('matricula',)