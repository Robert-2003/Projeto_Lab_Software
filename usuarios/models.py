from django.db import models
from django.contrib.auth.models import User, AbstractUser
from datetime import date
    

class Usuario(AbstractUser):
    class TipoUsuario(models.TextChoices):
        ADMINISTRADOR = 'adm', 'Administrador'
        TECNICO = 'tecnico', 'Técnico'
        CLIENTE = 'cliente', 'Cliente'

    matricula = models.CharField(
        unique=True, max_length=50, verbose_name='Matrícula'
    )
    tipo_usuario = models.CharField(
        choices=TipoUsuario.choices,
        max_length=10,
        default=TipoUsuario.ADMINISTRADOR,
        verbose_name='Tipo de Usuário'
    )
    data_cadastro = models.DateField(auto_now_add=True, verbose_name='Data de Cadastro')

    class Meta:
        db_table = 'usuario'
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.username

    def get_tipo_usuario_display(self):
        return self.get_tipo_usuario_display()