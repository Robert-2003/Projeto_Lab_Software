from django.contrib import admin
from django.urls import path, include
from usuarios import views
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='dashboard')),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('submit_login/', views.submit_login, name='submit_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/novo_usuario/', views.novo_usuario, name='novo_usuario'),
]