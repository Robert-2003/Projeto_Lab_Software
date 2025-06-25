from rolepermissions.roles import AbstractUserRole

class Administrador(AbstractUserRole):
    role_name = 'admin'
    display_name = 'Administrador'
    
    available_permissions = {
        'add_user',
        'change_user',
        'delete_user',
        'ver_todos_users',
    }
        
class Tecnico(AbstractUserRole):
    role_name = 'tecnico'
    display_name = 'Tecnico'
    
    available_permissions = {
        'ver_chamados_assumidos',
        'ver_chamados_disponiveis',
        'aceitar_chamados',
        'fechar_chamado',
        'desisitr_chamado',
        'alterar_chamado',
    }
    
class Cliente(AbstractUserRole):
    role_name = 'cliente'
    display_name = 'Cliente'
    
    available_permissions = {
        'criar_chamado',
        'alterar_chamado',
        'fechar_chamado',
        'reabir-chamado',
    }