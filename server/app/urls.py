# urls.py
from django.conf.urls import url
from app.views.viewsV import ClienteList, ClienteDetail,SolicitudList
from app.views.viewsC import Tecnicos, ProcesarSolicitud, ServicioList ,ServicioDetail,ProyectoCoordinador
from app.views.viewsT import ReporteInicial
from app.views.viewsAll import ListUsers,ValidarTrabajador,ValidarUsuario,ValidarCliente,CurrentUser,ValidarServicio
from rest_framework.authtoken import views


urlpatterns = [
    url(r'^cliente/$', ClienteList.as_view()),
    url(r'^cliente/(?P<pk>[\w\-]+)/$', ClienteDetail.as_view()),
    url(r'^api-token-auth/$', views.obtain_auth_token),
    url(r'^users/$', ListUsers.as_view()),
    url(r'^users/current/$', CurrentUser.as_view()),
    url(r'^validar/usuario/$', ValidarUsuario.as_view()),
    url(r'^validar/trabajador/$', ValidarTrabajador.as_view()),
    url(r'^validar/cliente/$', ValidarCliente.as_view()),
    url(r'^solicitud/$', SolicitudList.as_view()),

    url(r'^proyectos/tecnicos/$', Tecnicos.as_view()),
    url(r'^proyectos/solicitud/$', ProcesarSolicitud.as_view()),
    url(r'^servicio/$', ServicioList.as_view()),
    url(r'^servicio/(?P<pk>[\w\-]+)/$', ServicioDetail.as_view()),
    url(r'^validar/servicio/$', ValidarServicio.as_view()),
    url(r'^proyectoCoordinador/$', ProyectoCoordinador.as_view()),


    url(r'^proyecto/(?P<pk>[\w\-]+)/reporteInicial/$', ReporteInicial.as_view()),
]
