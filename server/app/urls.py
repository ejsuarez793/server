# urls.py
from django.conf.urls import url
from app.views.viewsV import ClienteList, ClienteDetail
from app.views.viewsAll import ListUsers,ValidarTrabajador,ValidarUsuario,CurrentUser
from rest_framework.authtoken import views


urlpatterns = [
    url(r'^clientes/$', ClienteList.as_view()),
    url(r'^clientes/(?P<pk>[\w\-]+)/$', ClienteDetail.as_view()),
    url(r'^api-token-auth/$', views.obtain_auth_token),
  #  url(r'^users/register/$', ListUsers.as_view()),
    url(r'^users/$', ListUsers.as_view()),
    url(r'^validar/usuario/$', ValidarUsuario.as_view()),
    url(r'^validar/trabajador/$', ValidarTrabajador.as_view()),
    url(r'^users/current/$', CurrentUser.as_view()),
]
