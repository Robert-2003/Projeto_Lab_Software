from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from usuarios import views as usuarios_views
from chamados import views as chamados_views
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='dashboard')),
    path('login/', usuarios_views.login_user, name='login'),
    path('logout/', usuarios_views.logout_user, name='logout'),
    path('submit_login/', usuarios_views.submit_login, name='submit_login'),
    path('dashboard/', usuarios_views.dashboard, name='dashboard'),
    path('dashboard/novo_usuario/', usuarios_views.novo_usuario, name='novo_usuario'),
    path('dashboard/<str:matricula>/', usuarios_views.usuario, name='usuario'),
    path('dashboard/<str:matricula>/editar/', usuarios_views.editar_usuario, name='editar_usuario'),
    path('dashboard/<str:matricula>/deletar/', usuarios_views.deletar_usuario, name='deletar_usuario'),
    path('criar/', chamados_views.criar_chamado, name='criar_chamado'),
    path('<int:id_protocolo>/', chamados_views.detalhe_chamado, name='detalhe_chamado'),
    path('<int:id_protocolo>/editar/', chamados_views.editar_chamado, name='editar_chamado'),
    path('<int:id_protocolo>/fechar/', chamados_views.fechar_chamado, name='fechar_chamado'),
    path('<int:id_protocolo>/reabrir/', chamados_views.reabrir_chamado, name='reabrir_chamado'),
    path('<int:id_protocolo>/deletar/', chamados_views.deletar_chamado, name='deletar_chamado'),
    path('<int:id_protocolo>/aceitar/', chamados_views.aceitar_chamado, name='aceitar_chamado'),
    path('<int:id_protocolo>/cancelar/', chamados_views.cancelar_chamado, name='cancelar_chamado'),
    path('<int:id_protocolo>/fechar/', chamados_views.fechar_chamado, name='fechar_chamado'),
    path('historico_tecnico/', chamados_views.historico_tecnico, name='historico_tecnico'),
    path('<int:id_protocolo>/editar_solucao/', chamados_views.editar_solucao, name='editar_solucao'),
    path('chamado/<str:id_protocolo>/remover_anexo_cliente/', chamados_views.remover_anexo_cliente, name='remover_anexo_cliente'),
    path('chamado/<str:id_protocolo>/remover_anexo_tecnico/', chamados_views.remover_anexo_tecnico, name='remover_anexo_tecnico'),
    path('chamado/<str:id_protocolo>/remover_anexo_solucao/', chamados_views.remover_anexo_solucao, name='remover_anexo_solucao'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)