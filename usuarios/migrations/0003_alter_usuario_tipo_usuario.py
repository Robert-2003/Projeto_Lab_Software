# Generated by Django 5.2.3 on 2025-06-28 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_alter_usuario_matricula'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='tipo_usuario',
            field=models.CharField(choices=[('adm', 'Administrador'), ('tecnico', 'Técnico'), ('cliente', 'Cliente')], max_length=20),
        ),
    ]
