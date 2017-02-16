# urls.py
from django.conf.urls import url
from rest_framework.authtoken import views


from app.views.viewsA import MaterialList, MaterialDetail, EquipoList, EquipoDetail, ProveedorList, ProveedorDetail, Disponibilidad, MovimientoIngreso, MovimientoEgreso, MovimientoRetorno, ConsultaRango, ValidarMaterial, ValidarProveedor
from app.views.viewsV import ClienteList, ClienteDetail, ResumenClientes, SolicitudList, ProyectoProcesarEstatus, ProyectoCausaRechazo, ProyectoEncuesta, FacturaEtapa, FacturaConsultar
from app.views.viewsC import ProyectoList, ProyectoDetail, ProyectoTecnicos, ReporteProyecto, ProyectoMaterialDesglose, SolicitudAprobar, ProyectoEtapa, ProyectoEtapaDetail, ActividadDetail, PresupuestoList, PresupuestoDetail, Tecnicos, ProcesarSolicitud, ServicioList, ServicioDetail, ProyectoCoordinador
from app.views.viewsT import ProyectosTecnico, ProyectoTecnico, EtapaTecnico, ActividadTecnico, SolicitudTecnico, ReporteInicial, ReporteDetalle, ReporteTecnico, SolicitudMaterial
from app.views.viewsAll import ListUsers, ValidarTrabajador, ValidarUsuario, ValidarCliente, CurrentUser, ValidarServicio
from app.views.viewsAdmin import GestionUsuario, ClaveUsuario




urlpatterns = [


    
    url(r'^login/$', views.obtain_auth_token),
    url(r'^usuario/actual/$', CurrentUser.as_view()),


    url(r'^validar/usuario/$', ValidarUsuario.as_view()),
    url(r'^validar/trabajador/$', ValidarTrabajador.as_view()),
    url(r'^validar/cliente/$', ValidarCliente.as_view()),
    url(r'^validar/servicio/$', ValidarServicio.as_view()),
    url(r'^validar/material/$', ValidarMaterial.as_view()),
    url(r'^validar/proveedor/$', ValidarProveedor.as_view()),



    url(r'^ventas/cliente/$', ClienteList.as_view()), # ESTA SE CAMBIO /cliente/ -->> /ventas/cliente/pk
    url(r'^ventas/cliente/(?P<pk>[\w\-]+)/$', ClienteDetail.as_view()), # ESTA SE CAMBIO /clientes/pk/ -->> /ventas/cliente/pk
    url(r'^ventas/solicitud/$', SolicitudList.as_view()), #ESTA SE CAMBIO /solicitud/ --> /ventas/solicitud/
    url(r'^ventas/factura/consultar/(?P<cod_eta>[\w\-]+)/(?P<cod_pre>[\w\-]+)/$', FacturaConsultar.as_view()),
    url(r'^ventas/factura/(?P<cod_eta>[\w\-]+)/$', FacturaEtapa.as_view()),
    url(r'^ventas/resumen/$', ResumenClientes.as_view()),


    url(r'^proyecto/(?P<pk>[\w\-]+)/estatus/$', ProyectoProcesarEstatus.as_view()),
    url(r'^proyecto/(?P<pk>[\w\-]+)/causaRechazo/$', ProyectoCausaRechazo.as_view()),
    url(r'^proyecto/(?P<pk>[\w\-]+)/encuesta/$', ProyectoEncuesta.as_view()),


    url(r'^proyecto/$', ProyectoList.as_view()),
    url(r'^proyecto/(?P<pk>[\w\-]+)/$', ProyectoDetail.as_view()),
    url(r'^proyecto/(?P<pk>[\w\-]+)/etapa/$', ProyectoEtapa.as_view()),
    url(r'^proyecto/(?P<pk_p>[\w\-]+)/etapa/(?P<pk_e>[\w\-]+)/$', ProyectoEtapaDetail.as_view()),
    url(r'^proyecto/(?P<pk_p>[\w\-]+)/etapa/(?P<pk_e>[\w\-]+)/actividad/$', ActividadDetail.as_view()),
    url(r'^proyecto/(?P<pk_p>[\w\-]+)/etapa/(?P<pk_e>[\w\-]+)/reporte/$', ReporteProyecto.as_view()),
    url(r'^proyecto/(?P<pk>[\w\-]+)/presupuesto/$', PresupuestoList.as_view()),
    url(r'^proyecto/(?P<pro_pk>[\w\-]+)/presupuesto/(?P<pre_pk>[\w\-]+)/$', PresupuestoDetail.as_view()),
    url(r'^proyecto/(?P<pk>[\w\-]+)/materiales/$', ProyectoMaterialDesglose.as_view()),
    url(r'^proyecto/(?P<pk>[\w\-]+)/solicitud/(?P<sol>[\w\-]+)/aprobar/$', SolicitudAprobar.as_view()),
    url(r'^proyecto/(?P<pk>[\w\-]+)/tecnico/$', ProyectoTecnicos.as_view()),
    
    url(r'^proyecto/coordinador/(?P<pk>[\w\-]+)/$', ProyectoCoordinador.as_view()),

    url(r'^coordinador/solicitud/procesar/$', ProcesarSolicitud.as_view()),
    url(r'^coordinador/servicio/$', ServicioList.as_view()), # ESTA SE CAMBIO /servicio/  ->> /coordinador/servicio/
    url(r'^coordinador/servicio/(?P<pk>[\w\-]+)/$', ServicioDetail.as_view()), #ESTA SE CAMBIO /servicio/pk/ --> /coordinador/servicio/pk/
    url(r'^coordinador/tecnicos/$', Tecnicos.as_view()), # ESTA SE CAMBIO /tecnicos/ --> coordinador/tecnicos/
    
   


    


    url(r'^almacen/disponibilidad/(?P<sol>[\w\-]+)/$', Disponibilidad.as_view()),
    url(r'^almacen/movimiento/ingreso/(?P<rif_prove>[\w\-]+)/$', MovimientoIngreso.as_view()),
    url(r'^almacen/movimiento/egreso/(?P<codigo_sol>[\w\-]+)/$', MovimientoEgreso.as_view()),
    url(r'^almacen/movimiento/retorno/(?P<codigo_pro>[\w\-]+)/$', MovimientoRetorno.as_view()),
    url(r'^almacen/consulta/(?P<tipo>[\w\-]+)/(?P<desde>[\w\-]+)/(?P<hasta>[\w\-]+)/$', ConsultaRango.as_view()),
    url(r'^almacen/material/$', MaterialList.as_view()),   #ESTA SE CAMBIO /material/  ->> /almacen/material/
    url(r'^almacen/material/(?P<pk>[\w\-]+)/$', MaterialDetail.as_view()),  # ESTA SE CAMBIO /material/pk/ -->> /almacen/material/pk
    url(r'^almacen/proveedor/$', ProveedorList.as_view()), #ESTA SE CAMBIO /proveedor/  ->> /almacen/proveedor/
    url(r'^almacen/proveedor/(?P<pk>[\w\-]+)/$', ProveedorDetail.as_view()),# ESTA SE CAMBIO /proveedor/pk/ -->> /almacen/proveedor/pk

   


   
    


    url(r'^tecnico/proyecto/(?P<pk>[\w\-]+)/reporteInicial/$', ReporteInicial.as_view()),
    url(r'^tecnico/proyecto/(?P<pk_p>[\w\-]+)/etapa/(?P<pk_e>[\w\-]+)/reporteDetalle/$', ReporteDetalle.as_view()),
    # url(r'^tecnico/proyecto/(?P<pk_p>[\w\-]+)/etapa/(?P<pk_e>[\w\-]+)/reporte/$', ReporteDetail.as_view()),
    url(r'^tecnico/proyectos/(?P<ci>[\w\-]+)/$', ProyectosTecnico.as_view()),
    url(r'^tecnico/proyecto/(?P<pk>[\w\-]+)/$', ProyectoTecnico.as_view()),
    url(r'^tecnico/proyecto/(?P<cod_pro>[\w\-]+)/etapa/(?P<cod_eta>[\w\-]+)/$', EtapaTecnico.as_view()),
    url(r'^tecnico/proyecto/(?P<cod_pro>[\w\-]+)/etapa/(?P<cod_eta>[\w\-]+)/actividad/$', ActividadTecnico.as_view()),
    url(r'^tecnico/solicitudes/(?P<ci>[\w\-]+)/$', SolicitudTecnico.as_view()),
    url(r'^tecnico/proyecto/(?P<codigo_pro>[\w\-]+)/etapa/(?P<codigo_eta>[\w\-]+)/solicitud/$', SolicitudMaterial.as_view()),
    url(r'^tecnico/proyecto/(?P<codigo_pro>[\w\-]+)/etapa/(?P<codigo_eta>[\w\-]+)/reporte/$', ReporteTecnico.as_view()),

    url(r'^admin/usuario/$', ListUsers.as_view()),
    url(r'^admin/gestion/(?P<ci>[\w\-]+)/$', GestionUsuario.as_view()),
    url(r'^admin/clave/(?P<ci>[\w\-]+)/$', ClaveUsuario.as_view()),
]

"""urlpatterns = [
    url(r'^cliente/$', ClienteList.as_view()),
    url(r'^cliente/(?P<pk>[\w\-]+)/$', ClienteDetail.as_view()),
    url(r'^api-token-auth/$', views.obtain_auth_token),
    url(r'^usuarios/$', ListUsers.as_view()),
    url(r'^users/current/$', CurrentUser.as_view()),
    url(r'^validar/usuario/$', ValidarUsuario.as_view()),
    url(r'^validar/trabajador/$', ValidarTrabajador.as_view()),
    url(r'^validar/cliente/$', ValidarCliente.as_view()),
    url(r'^validar/servicio/$', ValidarServicio.as_view()),
    url(r'^solicitud/$', SolicitudList.as_view()),
    url(r'^proyecto/(?P<pk>[\w\-]+)/estatus/$', ProyectoProcesarEstatus.as_view()),
    url(r'^proyecto/(?P<pk>[\w\-]+)/causaRechazo/$', ProyectoCausaRechazo.as_view()),
    url(r'^proyecto/(?P<pk>[\w\-]+)/encuesta/$', ProyectoEncuesta.as_view()),


    url(r'^proyecto/$', ProyectoList.as_view()),
    url(r'^proyecto/(?P<pk>[\w\-]+)/$', ProyectoDetail.as_view()),
    url(r'^proyecto/(?P<pk>[\w\-]+)/etapa/$', ProyectoEtapa.as_view()),
    url(r'^proyecto/(?P<pk_p>[\w\-]+)/etapa/(?P<pk_e>[\w\-]+)/$', ProyectoEtapaDetail.as_view()),
    url(r'^proyecto/(?P<pk_p>[\w\-]+)/etapa/(?P<pk_e>[\w\-]+)/actividad/$', ActividadDetail.as_view()),
    url(r'^proyecto/(?P<pk_p>[\w\-]+)/etapa/(?P<pk_e>[\w\-]+)/reporte/$', ReporteProyecto.as_view()),
    # url(r'^proyecto/(?P<pk_p>[\w\-]+)/etapa/(?P<pk_e>[\w\-]+)/solicitud/$', SolicitudMaterialDetail.as_view()),
    url(r'^proyecto/(?P<pk>[\w\-]+)/presupuesto/$', PresupuestoList.as_view()),
    url(r'^proyecto/(?P<pro_pk>[\w\-]+)/presupuesto/(?P<pre_pk>[\w\-]+)/$', PresupuestoDetail.as_view()),
    url(r'^proyecto/(?P<pk>[\w\-]+)/materiales/$', ProyectoMaterialDesglose.as_view()),
    url(r'^proyecto/(?P<pk>[\w\-]+)/solicitud/(?P<sol>[\w\-]+)/aprobar/$', SolicitudAprobar.as_view()),
    url(r'^tecnicos/$', Tecnicos.as_view()),
    url(r'^proyecto/(?P<pk>[\w\-]+)/tecnico/$', ProyectoTecnicos.as_view()),
    url(r'^solicitud/procesar/$', ProcesarSolicitud.as_view()),
    url(r'^servicio/$', ServicioList.as_view()),
    url(r'^servicio/(?P<pk>[\w\-]+)/$', ServicioDetail.as_view()),
    
    url(r'^proyecto/coordinador/(?P<pk>[\w\-]+)/$', ProyectoCoordinador.as_view()),


    


    url(r'^almacen/disponibilidad/(?P<sol>[\w\-]+)/$', Disponibilidad.as_view()),
    url(r'^almacen/movimiento/ingreso/(?P<rif_prove>[\w\-]+)/$', MovimientoIngreso.as_view()),
    url(r'^almacen/movimiento/egreso/(?P<codigo_sol>[\w\-]+)/$', MovimientoEgreso.as_view()),
    url(r'^almacen/movimiento/retorno/(?P<codigo_pro>[\w\-]+)/$', MovimientoRetorno.as_view()),
    url(r'^almacen/consulta/(?P<tipo>[\w\-]+)/(?P<desde>[\w\-]+)/(?P<hasta>[\w\-]+)/$', ConsultaRango.as_view()),
    

    url(r'^ventas/factura/consultar/(?P<cod_eta>[\w\-]+)/(?P<cod_pre>[\w\-]+)/$', FacturaConsultar.as_view()),
    url(r'^ventas/factura/(?P<cod_eta>[\w\-]+)/$', FacturaEtapa.as_view()),
    url(r'^ventas/resumen/$', ResumenClientes.as_view()),
    url(r'^material/$', MaterialList.as_view()),
    url(r'^material/(?P<pk>[\w\-]+)/$', MaterialDetail.as_view()),
    url(r'^validar/material/$', ValidarMaterial.as_view()),
    url(r'^equipo/$', EquipoList.as_view()),
    url(r'^equipo/(?P<pk>[\w\-]+)/$', EquipoDetail.as_view()),
    url(r'^proveedor/$', ProveedorList.as_view()),
    url(r'^proveedor/(?P<pk>[\w\-]+)/$', ProveedorDetail.as_view()),
    url(r'^validar/proveedor/$', ValidarProveedor.as_view()),


    url(r'^tecnico/proyecto/(?P<pk>[\w\-]+)/reporteInicial/$', ReporteInicial.as_view()),
    url(r'^tecnico/proyecto/(?P<pk_p>[\w\-]+)/etapa/(?P<pk_e>[\w\-]+)/reporteDetalle/$', ReporteDetalle.as_view()),
    # url(r'^tecnico/proyecto/(?P<pk_p>[\w\-]+)/etapa/(?P<pk_e>[\w\-]+)/reporte/$', ReporteDetail.as_view()),
    url(r'^tecnico/proyectos/(?P<ci>[\w\-]+)/$', ProyectosTecnico.as_view()),
    url(r'^tecnico/proyecto/(?P<pk>[\w\-]+)/$', ProyectoTecnico.as_view()),
    url(r'^tecnico/proyecto/(?P<cod_pro>[\w\-]+)/etapa/(?P<cod_eta>[\w\-]+)/$', EtapaTecnico.as_view()),
    url(r'^tecnico/proyecto/(?P<cod_pro>[\w\-]+)/etapa/(?P<cod_eta>[\w\-]+)/actividad/$', ActividadTecnico.as_view()),
    url(r'^tecnico/solicitudes/(?P<ci>[\w\-]+)/$', SolicitudTecnico.as_view()),
    url(r'^tecnico/proyecto/(?P<codigo_pro>[\w\-]+)/etapa/(?P<codigo_eta>[\w\-]+)/solicitud/$', SolicitudMaterial.as_view()),
    url(r'^tecnico/proyecto/(?P<codigo_pro>[\w\-]+)/etapa/(?P<codigo_eta>[\w\-]+)/reporte/$', ReporteTecnico.as_view()),

    url(r'^admin/gestion/(?P<ci>[\w\-]+)/$', GestionUsuario.as_view()),
    url(r'^admin/clave/(?P<ci>[\w\-]+)/$', ClaveUsuario.as_view()),
]"""
