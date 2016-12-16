# urls.py
from django.conf.urls import url
from rest_framework.authtoken import views


from app.views.viewsA import MaterialList, MaterialDetail, EquipoList, EquipoDetail,ProveedorList, ProveedorDetail
from app.views.viewsV import ClienteList, ClienteDetail,SolicitudList
from app.views.viewsC import ProyectoList, ProyectoDetail, PresupuestoList, Tecnicos, ProcesarSolicitud, ServicioList ,ServicioDetail,ProyectoCoordinador
from app.views.viewsT import ReporteInicial
from app.views.viewsAll import ListUsers,ValidarTrabajador,ValidarUsuario,ValidarCliente,CurrentUser,ValidarServicio



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

    url(r'^proyecto/$', ProyectoList.as_view()),
    url(r'^proyecto/(?P<pk>[\w\-]+)/$', ProyectoDetail.as_view()),
    url(r'^proyecto/(?P<pk>[\w\-]+)/presupuesto/$', PresupuestoList.as_view()),
    url(r'^tecnicos/$', Tecnicos.as_view()),
    url(r'^solicitud/procesar/$', ProcesarSolicitud.as_view()),
    url(r'^servicio/$', ServicioList.as_view()),
    url(r'^servicio/(?P<pk>[\w\-]+)/$', ServicioDetail.as_view()),
    url(r'^validar/servicio/$', ValidarServicio.as_view()),
    url(r'^proyecto/coordinador/(?P<pk>[\w\-]+)/$', ProyectoCoordinador.as_view()),


    url(r'^proyecto/(?P<pk>[\w\-]+)/reporteInicial/$', ReporteInicial.as_view()),


    url(r'^material/$', MaterialList.as_view()),
    url(r'^material/(?P<pk>[\w\-]+)/$', MaterialDetail.as_view()),
    url(r'^equipo/$', EquipoList.as_view()),
    url(r'^equipo/(?P<pk>[\w\-]+)/$', EquipoDetail.as_view()),
    url(r'^proveedor/$', ProveedorList.as_view()),
    url(r'^proveedor/(?P<pk>[\w\-]+)/$', ProveedorDetail.as_view()),
]
