from django.db import models
from django.contrib.auth.models import User, AbstractUser
from datetime import date
    
TIPOS_USUARIO = (
    ('adm', 'Administrador'),
    ('tecnico', 'Técnico'),
    ('cliente', 'Cliente'),
)

class Usuario(AbstractUser):
    matricula = models.CharField(
        unique=True, max_length=50, verbose_name='Matrícula', blank=True
    )
    tipo_usuario = models.CharField(max_length=20, choices=TIPOS_USUARIO)
    data_cadastro = models.DateField(auto_now_add=True, verbose_name='Data de Cadastro')
    
    USERNAME_FIELD = 'matricula'
    REQUIRED_FIELDS = ['username', 'password']

    class Meta:
        db_table = 'usuario'
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_data_cadastro(self):
        return self.data_cadastro.strftime('%d/%m/%Y')