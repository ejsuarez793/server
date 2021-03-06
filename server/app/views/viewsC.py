#from django.contrib.auth.models import User
from app.models import Trabajador, Solicitud, Servicio,Proyecto, Factura, Etapa, Actividad, Reporte_detalle, Reporte, Reporte_servicio, Causa_rechazo, Encuesta, Pregunta, Movimiento, Etapa_tecnico_movimiento, Material_movimiento, Material, Cliente,Reporte_inicial,Presupuesto, Servicio_presupuesto, Material_presupuesto, Proyecto_tecnico
from app.serializers.serializersAll import TrabajadorSerializer
from app.serializers.serializersV import ClienteSerializer
from app.serializers.serializersC import ProyectoSerializer,ProyectoEstatusSerializer, ProyectoSerializerPG, EtapaSerializer, ActividadSerializer, ReporteDetalleSerializer, ReporteSerializer, PresupuestoSerializer, Causa_rechazoSerializer, PreguntaSerializer, EncuestaSerializer, MaterialSerializer, Servicio_presupuestoSerializer, Material_presupuestoSerializer, SolicitudSerializer, SolicitudSerializerAll, ProyectoTecnicoSerializer, ServicioSerializer, ReporteInicialSerializer
from django.db import transaction
from rest_framework.permissions import (
    #AllowAny,
    IsAuthenticated,
    #IsAdminUser,
    #IsAuthenticatedOrReadOnly,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from app.permissions import esCoordinador, esCoordinadorOesVendedor


def viewsCoordinador(arg):
    pass


class ProyectoList(APIView):
    permission_classes = [IsAuthenticated, esCoordinador]

    def get(self, request, format=None):
        proyectos = Proyecto.objects.all().order_by('codigo')
        s_proyectos = ProyectoSerializer(proyectos, many=True)
        for proyecto in s_proyectos.data:
            solicitud = Solicitud.objects.get(codigo=proyecto['codigo_s'])
            s_solicitud = SolicitudSerializerAll(solicitud)
            cliente = Cliente.objects.get(rif=s_solicitud.data['rif_c'])
            s_cliente = ClienteSerializer(cliente)
            proyecto['nombre_c'] = s_cliente.data['nombre']
        return Response(s_proyectos.data, status=status.HTTP_200_OK)


class ProyectoDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        proyecto = Proyecto.objects.get(codigo=pk)
        s_proyecto = ProyectoSerializer(proyecto)

        solicitud = Solicitud.objects.get(codigo=s_proyecto.data['codigo_s'])
        s_solicitud = SolicitudSerializerAll(solicitud)

        cliente = Cliente.objects.get(rif=s_solicitud.data['rif_c'])
        s_cliente = ClienteSerializer(cliente)

        presupuestos = Presupuesto.objects.filter(codigo_pro=s_proyecto.data['codigo']).order_by('codigo')
        s_presupuestos = PresupuestoSerializer(presupuestos, many=True)
        for presupuesto in s_presupuestos.data:
            servicios = Servicio_presupuesto.objects.filter(codigo_pre=presupuesto['codigo'])
            s_servicios = Servicio_presupuestoSerializer(servicios, many=True)
            presupuesto['servicios'] = s_servicios.data
            for servicio in presupuesto['servicios']:
                ser = Servicio.objects.get(codigo=servicio['codigo_ser'])
                s_ser = ServicioSerializer(ser)
                servicio['desc'] = s_ser.data['desc']

            materiales = Material_presupuesto.objects.filter(codigo_pre=presupuesto['codigo'])
            s_materiales = Material_presupuestoSerializer(materiales, many=True)
            presupuesto['materiales'] = s_materiales.data
            for material in presupuesto['materiales']:
                mat = Material.objects.get(codigo=material['codigo_mat'])
                s_mat = MaterialSerializer(mat)
                material['desc'] = s_mat.data['nombre'] + " " + s_mat.data['desc'] + " " + s_mat.data['marca'] + " (" + s_mat.data['presen'] + ")"

        proyecto = s_proyecto.data
        proyecto['cliente'] = s_cliente.data
        proyecto['contacto'] = s_solicitud.data
        proyecto['presupuestos'] = s_presupuestos.data

        tecnicos = Proyecto_tecnico.objects.filter(codigo_pro=pk)
        proyecto['tecnicos'] = []
        for tecnico in tecnicos:
            aux= {}
            aux['ci'] = tecnico.ci_tecnico.ci
            aux['nombre'] = tecnico.ci_tecnico.nombre1 + " " + tecnico.ci_tecnico.nombre2 + " " + tecnico.ci_tecnico.apellido1 + " " + tecnico.ci_tecnico.apellido2            
            aux['tlf'] = tecnico.ci_tecnico.tlf
            aux['correo'] = tecnico.ci_tecnico.correo
            proyecto['tecnicos'].append(aux)
        try:
            causa_rechazo = Causa_rechazo.objects.get(codigo_pro=s_proyecto.data['codigo'])
            s_causa_rechazo = Causa_rechazoSerializer(causa_rechazo)
            proyecto['causa_rechazo'] = s_causa_rechazo.data
        except Causa_rechazo.DoesNotExist:
            proyecto['causa_rechazo'] = None

        try:
            etapas = Etapa.objects.filter(codigo_pro=s_proyecto.data['codigo']).order_by('codigo')
            s_etapas = EtapaSerializer(etapas, many=True)
            solicitudes = []
            try:
                for etapa in s_etapas.data:
                    reporte_detalle = Reporte_detalle.objects.get(codigo=etapa['codigo_rd'])
                    s_reporte_detalle = ReporteDetalleSerializer(reporte_detalle)
                    etapa['reporte_detalle'] = s_reporte_detalle.data
                    reportes = Reporte.objects.filter(codigo_eta=etapa['codigo']).order_by('codigo')
                    s_reportes = ReporteSerializer(reportes, many=True)
                    for reporte in s_reportes.data:
                        rep_sev = Reporte_servicio.objects.filter(codigo_rep=reporte['codigo'])
                        reporte['servicios'] = []
                        for rs in rep_sev:
                            aux = {}
                            aux['codigo'] = rs.codigo_ser.codigo
                            aux['desc'] = rs.codigo_ser.desc
                            aux['cantidad'] = rs.cantidad
                            reporte['servicios'].append(aux)

                    etapa['reportes'] = s_reportes.data

                    actividades = Actividad.objects.filter(codigo_eta=etapa['codigo'])
                    s_actividades = ActividadSerializer(actividades, many=True)
                    etapa['actividades'] = s_actividades.data

                    etms = Etapa_tecnico_movimiento.objects.filter(codigo_eta=etapa['codigo']).order_by('codigo')
                    for etm in etms:
                        if (etm.codigo_mov.tipo == "Egreso"):
                            aux = {}
                            aux['codigo'] = etm.codigo_mov.codigo
                            aux['nombre_t'] = etm.ci_tecnico.nombre1 + " " + etm.ci_tecnico.apellido1
                            aux['ci_tecnico'] = etm.ci_tecnico.ci
                            aux['f_sol'] = etm.codigo_mov.f_sol
                            aux['letra_eta'] = etm.codigo_eta.letra
                            aux['nombre_eta'] = etm.codigo_eta.nombre
                            aux['autorizado'] = etm.codigo_mov.autorizado
                            aux['completado'] = etm.codigo_mov.completado
                            mm = Material_movimiento.objects.filter(codigo_mov=etm.codigo_mov.codigo)
                            aux['materiales'] = []
                            for material in mm:
                                aux_2 = {}
                                aux_2['codigo_mat'] = material.codigo_mat.codigo
                                aux_2['nombre_mat'] = material.codigo_mat.nombre
                                aux_2['desc_mat'] = material.codigo_mat.desc
                                aux_2['marca_mat'] = material.codigo_mat.marca
                                aux_2['presen_mat'] = material.codigo_mat.presen
                                aux_2['serial_mat'] = material.codigo_mat.serial
                                aux_2['cant'] = material.cantidad
                                aux['materiales'].append(aux_2)
                            solicitudes.append(aux)
                    proyecto['solicitudes'] = solicitudes
            except Reporte_detalle.DoesNotExist:
                etapa['reporte_detalle'] = None
            proyecto['etapas'] = s_etapas.data
        except Etapa.DoesNotExist:
            proyecto['etapas'] = None

        try:
            encuesta = Encuesta.objects.get(codigo_pro=s_proyecto.data['codigo'])
            s_encuesta = EncuestaSerializer(encuesta)
            preguntas = Pregunta.objects.filter(codigo_en=s_encuesta.data['codigo'])
            s_preguntas = PreguntaSerializer(preguntas, many=True)
            proyecto['encuesta'] = s_encuesta.data
            proyecto['encuesta']['preguntas'] = s_preguntas.data
        except (Causa_rechazo.DoesNotExist, Encuesta.DoesNotExist):
            proyecto['encuesta'] = None

        return Response(proyecto, status=status.HTTP_200_OK)

    def patch(self, request, pk, format=None):
        try:
            proyecto = Proyecto.objects.get(codigo=pk)

            if (proyecto.codigo_ri is None and request.data['accion'] == "Iniciar"):
                return Response("Se debe completar el reporte inicial para iniciar el proyecto", status=status.HTTP_400_BAD_REQUEST)

            s_proyecto = ProyectoSerializerPG(proyecto, data=request.data)
            if (s_proyecto.is_valid(raise_exception=True)):
                data = {}
                etapas = Etapa.objects.filter(codigo_pro=pk)
                if(s_proyecto.initial_data['accion'] == "Iniciar"):
                    data['msg'] = "Proyecto iniciado exitosamente."
                    pts = Proyecto_tecnico.objects.filter(codigo_pro=pk)
                    if not pts:
                        return Response("Debes asignar al menos 1 tecnico al proyecto.", status=status.HTTP_400_BAD_REQUEST)
                    if not etapas:
                        return Response("Debes definir al menos 1 etapa en el proyecto.", status=status.HTTP_400_BAD_REQUEST)
                elif(s_proyecto.initial_data['accion'] == "Culminar"):
                    data['msg'] = "Proyecto culminado exitosamente."
                    for etapa in etapas:
                        if (etapa.estatus != "Culminado"):
                            return Response("Hay etapas que no han sido culminadas.", status=status.HTTP_400_BAD_REQUEST)
                else:
                    data['msg'] = "Proyecto editado exitosamente!"
                s_proyecto.save()
                data['data'] = s_proyecto.data
                return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        try:
            with transaction.atomic():
                proyecto = Proyecto.objects.get(codigo=pk)
                if(proyecto.estatus == "Preventa"):
                    s_proyecto = ProyectoEstatusSerializer(proyecto, data=request.data)
                    if(s_proyecto.is_valid(raise_exception=True)):
                        presupuestos = Presupuesto.objects.filter(codigo_pro=s_proyecto.validated_data['codigo'])
                        s_presupuestos = PresupuestoSerializer(presupuestos, many=True)
                        if(s_proyecto.validated_data['estatus'] == "Aprobado"):
                            flag = False
                            for presupuesto in s_presupuestos.data:
                                if (presupuesto['estatus'] == "Preventa"):
                                    return Response("Proyecto tiene un presupuesto que sigue en preventa", status=status.HTTP_400_BAD_REQUEST)
                            for presupuesto in s_presupuestos.data:
                                if (presupuesto['estatus'] == "Rechazado"):
                                    # print("p")
                                    Material_presupuesto.objects.filter(codigo_pre=presupuesto['codigo']).delete()
                                    Servicio_presupuesto.objects.filter(codigo_pre=presupuesto['codigo']).delete()
                                    Presupuesto.objects.get(codigo=presupuesto['codigo']).delete()

                        elif(s_proyecto.validated_data['estatus'] == "Rechazado"):
                            flag = False
                            for presupuesto in s_presupuestos.data:
                                if (presupuesto['estatus'] != "Rechazado"):
                                    flag = True
                            if (flag is True):
                                return Response("Proyecto tiene un presupuesto que no ha sido rechazado", status=status.HTTP_400_BAD_REQUEST)
                        s_proyecto.save()
                        msg = "Proyecto " + s_proyecto.validated_data['estatus'] + " Exitosamente!"
                        data = {}
                        data['data'] = s_proyecto.data
                        data['msg'] = msg
                        return Response(data, status=status.HTTP_200_OK)
                else:
                    return Response("El estado del proyecto no permite realizar dicha accion.", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class ProyectoEtapa(APIView):
    permissions_classes = [IsAuthenticated, esCoordinador]

    def post(self, request, pk, format=None):
        try:
            proyecto = Proyecto.objects.get(codigo=pk)
            if (proyecto.estatus == "Preventa" or proyecto.estatus == "Rechazado" or proyecto.estatus == "Culminado"):
                return Response("El estado del proyecto '" + proyecto.estatus + "' no permite crear una etapa.", status=status.HTTP_400_BAD_REQUEST)

            s_etapa = EtapaSerializer(data=request.data)
            if(s_etapa.is_valid(raise_exception=True)):
                s_etapa.save()
                data = {}
                data['data'] = s_etapa.data
                data['msg'] = "Etapa creada exitosamente!"
                return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class ProyectoEtapaDetail(APIView):
    permissions_classes = [IsAuthenticated, esCoordinador]

    def patch(self, request, pk_p, pk_e, format=None):
        try:
            etapa = Etapa.objects.get(codigo=pk_e)
            s_etapa = EtapaSerializer(etapa, data=request.data)
            if(s_etapa.is_valid(raise_exception=True)):
                data = {}
                actividades = Actividad.objects.filter(codigo_eta=pk_e)
                if (s_etapa.initial_data['accion'] == "Iniciar"):
                    proyecto = Proyecto.objects.get(codigo=pk_p)
                    if (proyecto.estatus != "Ejecucion"):
                        return Response("El proyecto debe estar en ejecucion para iniciar etapa.", status=status.HTTP_400_BAD_REQUEST)
                    etapa = Etapa.objects.get(codigo=pk_e)
                    if (etapa.codigo_rd is None):
                        return Response("El reporte de detalle debe ser completado.", status=status.HTTP_400_BAD_REQUEST)
                    if not actividades:
                        return Response("Debes definir al menos 1 actividad.", status=status.HTTP_400_BAD_REQUEST)
                    data['msg'] = "Etapa iniciada exitosamente!"
                elif(s_etapa.initial_data['accion'] == "Culminar"):
                    for actividad in actividades:
                        if (actividad.completada is False):
                            return Response("Hay actividades que no han sido completadas.", status=status.HTTP_400_BAD_REQUEST)
                    reportes = Reporte.objects.filter(codigo_eta=pk_e)
                    for reporte in reportes:
                        if (reporte.leido is False):
                            return Response("Hay reportes que no han sido leidos y verificados.", status=status.HTTP_400_BAD_REQUEST)
                    data['msg'] = "Etapa culminada exitosamente!"
                else:
                    data['msg'] = "Etapa editada exitosamente!"
                s_etapa.save()
                data['data'] = s_etapa.data
                return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class ActividadDetail(APIView):
    permissions_classes = [IsAuthenticated, esCoordinador]

    def post(self, request, pk_p, pk_e, format=None):
        try:
            # print(request.data)
            s_actividad = ActividadSerializer(data=request.data, many=True)
            if (s_actividad.is_valid(raise_exception=True)):
                s_actividad.save()
                data = {}
                data['data'] = s_actividad.data
                data['msg'] = "Actividades definidas exitosamente!"
                return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class ReporteProyecto(APIView):
    permissions_classes = [IsAuthenticated, esCoordinador]

    def patch(self, request, pk_p, pk_e, format=None):
        try:
            with transaction.atomic():
                for reporte in request.data:
                    rep = Reporte.objects.get(codigo=reporte['codigo'])
                    rep.leido = True
                    rep.save()
                    print(reporte['codigo'])
                    rep_serv = Reporte_servicio.objects.filter(codigo_rep=reporte['codigo'])
                    for rs in rep_serv:
                        for servicio in reporte['servicios']:
                            if (servicio == rs.codigo_ser.codigo):
                                rs.delete()
                                # print(servicio)
                                # print("entro! borrar: "+str(reporte['codigo'])+" y serv: "+str(servicio))

                data = {}
                data['data'] = request.data
                data['msg'] = "Reportes marcados como leidos exitosamente!"
                return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class ProyectoMaterialDesglose(APIView):
    permissions_classes = [IsAuthenticated]  # aqui falta poner esCoordinadoroALmacenista o dejarlo asi

    def get(self, request, pk, format=None):
        data_desglose = {}
        data_presupuesto = []
        #data_egresados = []
        #data_retornados = []
        data_usados = []
        data_usados_etapas = []
        aux = {}
        aux_2 = {}
        codigo_presupuesto = ""
        materiales_aux = []

        # primero buscamos los materiales que estan en el presupuesto aprobado del proyecto
        presupuestos = Presupuesto.objects.filter(codigo_pro=pk).order_by('codigo')
        for presupuesto in presupuestos:
            if (presupuesto.estatus == "Aprobado"):
                codigo_presupuesto = presupuesto.codigo
                break

        materiales_presupuesto = Material_presupuesto.objects.filter(codigo_pre=codigo_presupuesto)
        for material_presupuesto in materiales_presupuesto:
            aux = {}
            # aux['codigo_pre'] = presupuesto.codigo
            aux['codigo'] = material_presupuesto.codigo_mat.codigo
            aux['nombre'] = material_presupuesto.codigo_mat.nombre
            aux['desc'] = material_presupuesto.codigo_mat.desc
            aux['serial'] = material_presupuesto.codigo_mat.serial
            aux['marca'] = material_presupuesto.codigo_mat.marca
            aux['presen'] = material_presupuesto.codigo_mat.presen
            aux['cantidad'] = material_presupuesto.cantidad
            data_presupuesto.append(aux)

        # luego buscamos los materiales usados por etapas, y si la etapa se considera que esta bajo el presupuesto
        # actual, se considera para restar sus elementos posteriormente
        etapas = Etapa.objects.filter(codigo_pro=pk).order_by('codigo')
        for etapa in etapas:
            aux = {}
            aux['letra_eta'] = etapa.letra
            aux['nombre_eta'] = etapa.nombre
            aux['codigo_eta'] = etapa.codigo
            aux['materiales'] = []

            # aqui consideramos si los materiales de la etapa entran para restar los disponibles segun presupuesto actual
            considerar = False
            if (etapa.facturada is False):
                considerar = True
            else:
                factura = Factura.objects.get(codigo_eta=etapa.codigo)
                if (factura.codigo_pre.codigo == codigo_presupuesto):
                    considerar = True
            aux['considerar'] = considerar

            etms = Etapa_tecnico_movimiento.objects.filter(codigo_eta=etapa.codigo)
            for etm in etms:
                if (etm.codigo_mov.completado is True):
                    mm = Material_movimiento.objects.filter(codigo_mov=etm.codigo_mov.codigo)
                    for material in mm:
                        aux_2 = {}
                        aux_2['codigo'] = material.codigo_mat.codigo
                        aux_2['nombre'] = material.codigo_mat.nombre
                        aux_2['desc'] = material.codigo_mat.desc
                        aux_2['marca'] = material.codigo_mat.marca
                        aux_2['serial'] = material.codigo_mat.serial
                        aux_2['presen'] = material.codigo_mat.presen
                        aux_2['cantidad'] = material.cantidad
                        if (etm.codigo_mov.tipo == "Retorno"):  # aqui retorno es negativo ya que queremos que se muestren los usados como positivos
                            aux_2['cantidad'] *= -1             # y los retornados restan su valor a los usados

                        yaAgregado = False
                        for material_agregado in aux['materiales']:
                            if (material_agregado['codigo'] == aux_2['codigo']):
                                yaAgregado = True
                                material_agregado['cantidad'] += aux_2['cantidad']

                        if (yaAgregado is False):
                            aux['materiales'].append(aux_2)
            if not aux['materiales']:
                aux['tiene_materiales'] = False
            else:
                aux['tiene_materiales'] = True
            data_usados_etapas.append(aux)

        # ahora sumamos todos los materiales usados por etapas, y si las etapas estan bajo consideracion del presupuesto
        # actual se le restan a los materiales disponibles actuales, es decir, si son materiales que se han usado
        # del presupuesto que esta disponible actualmente, se le deben restar las cantidades usadas a las disp.
        for etapa in data_usados_etapas:
            for material in etapa['materiales']:

                if(etapa['considerar'] is True):
                    for material_disponible in data_presupuesto:
                        if (material_disponible['codigo'] == material['codigo']):
                            material_disponible['cantidad'] -= material['cantidad']

                yaAgregado = False
                for material_agregado in data_usados:
                    if (material_agregado['codigo'] == material['codigo']):
                        material_agregado['cantidad'] += material['cantidad']
                        yaAgregado = True
                if (yaAgregado is False):
                    aux = {}
                    aux['codigo'] = material['codigo']
                    aux['nombre'] = material['nombre']
                    aux['desc'] = material['desc']
                    aux['marca'] = material['marca']
                    aux['serial'] = material['serial']
                    aux['presen'] = material['presen']
                    aux['cantidad'] = material['cantidad']
                    data_usados.append(aux)

        # print(data_presupuesto)
        # print(data_usados_etapas)
        # print(data_usados)

        # por ultimo eliminamos las cantidades en 0
        data_desglose['disponibles'] = []
        data_desglose['usados'] = []
        data_desglose['etapas'] = []

        for material in data_presupuesto:
            if (material['cantidad'] != 0):
                data_desglose['disponibles'].append(material)

        for material in data_usados:
            if (material['cantidad'] != 0):
                data_desglose['usados'].append(material)

        for etapa in data_usados_etapas:
            aux = {}
            aux['letra_eta'] = etapa['letra_eta']
            aux['nombre_eta'] = etapa['nombre_eta']
            aux['codigo_eta'] = etapa['codigo_eta']
            aux['considerar'] = etapa['considerar']
            aux['tiene_materiales'] = etapa['tiene_materiales']
            aux['materiales'] = []
            for material in etapa['materiales']:
                if(material['cantidad'] != 0):
                    aux['materiales'].append(material)
            data_desglose['etapas'].append(aux)

        # print(data_desglose)
        return Response(data_desglose, status=status.HTTP_200_OK)


class SolicitudAprobar(APIView):
    permissions_classes = [IsAuthenticated, esCoordinador]

    def post(self, request, pk, sol, format=None):
        movimiento = Movimiento.objects.get(codigo=sol)
        movimiento.autorizado = request.data
        movimiento.save()
        data = {}
        data['data'] = None
        data['msg'] = "Solicitud de material aprobada exitosamente."
        return Response(data, status=status.HTTP_200_OK)


class PresupuestoList(APIView):
    permission_classes = [IsAuthenticated, esCoordinador]

    def post(self, request, pk, format=None):
        try:
            with transaction.atomic():
                proyecto = Proyecto.objects.get(codigo=pk)
                if (proyecto.estatus == "Culminado" or proyecto.estatus == "Rechazado"):
                    return Response("El estado del proyecto no permite solicitar un presupuesto.", status=status.HTTP_400_BAD_REQUEST)

                # revisamos que todos los presupuestos anteriores se encuentren cerrados.
                presupuestos = Presupuesto.objects.filter(codigo_pro=pk)
                noCerrado = False
                for presupuesto in presupuestos:
                    if (presupuesto.estatus != "Cerrado"):
                        noCerrado = True
                if (noCerrado is True):
                    return Response("Para solicitar otro presupuesto, el anterior debe estar cerrado.", status=status.HTTP_400_BAD_REQUEST)

                s_presupuesto = PresupuestoSerializer(data=request.data)
                if (s_presupuesto.is_valid(raise_exception=True)):
                    s_presupuesto.save()
                    print(s_presupuesto.validated_data)

                    for servicio in request.data['servicios']:
                        servicio['codigo_ser'] = servicio['codigo']
                        servicio['codigo_pre'] = s_presupuesto.validated_data['codigo']
                        s_servicio = Servicio_presupuestoSerializer(data=servicio)
                        if (s_servicio.is_valid(raise_exception=True)):
                            s_servicio.save()

                    for material in request.data['materiales']:
                        material['codigo_mat'] = material['codigo']
                        material['codigo_pre'] = s_presupuesto.validated_data['codigo']
                        s_material = Material_presupuestoSerializer(data=material)
                        if (s_material.is_valid(raise_exception=True)):
                            s_material.save()

                data = {}
                data['data'] = request.data
                data['msg'] = "Presupuesto solicitado exitosamente."
                return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class PresupuestoDetail(APIView):
    permission_classes = [IsAuthenticated, esCoordinadorOesVendedor]

    def patch(self, request, pro_pk, pre_pk, format=None):  # este verbo lo usa el coordinador para editar los mat y serv del presupuesto

        try:
            with transaction.atomic():
                proyecto = Proyecto.objects.get(codigo=pro_pk)
                if (proyecto.estatus == "Rechazado" or proyecto.estatus == "Culminado"):
                    return Response("El estado del proyecto no permite editar el presupuesto.", status=status.HTTP_400_BAD_REQUEST)
                presupuesto = Presupuesto.objects.get(codigo=pre_pk)
                if(presupuesto.estatus != "Aprobado" and presupuesto.estatus != "Cerrado"):
                    s_presupuesto = PresupuestoSerializer(presupuesto, data=request.data)
                    if(s_presupuesto.is_valid(raise_exception=True)):
                        s_presupuesto.save()
                        Servicio_presupuesto.objects.filter(codigo_pre=pre_pk).delete()
                        for servicio in request.data['servicios']:
                            servicio['codigo_ser'] = servicio['codigo']
                            servicio['codigo_pre'] = s_presupuesto.validated_data['codigo']
                            s_servicio = Servicio_presupuestoSerializer(data=servicio)
                            if (s_servicio.is_valid(raise_exception=True)):
                                s_servicio.save()
                        Material_presupuesto.objects.filter(codigo_pre=pre_pk).delete()
                        for material in request.data['materiales']:
                            material['codigo_mat'] = material['codigo']
                            material['codigo_pre'] = s_presupuesto.validated_data['codigo']
                            s_material = Material_presupuestoSerializer(data=material)
                            if (s_material.is_valid(raise_exception=True)):
                                s_material.save()
                    data = {}
                    data['data'] = request.data
                    data['msg'] = "Presupuesto editado exitosamente."
                else:
                    return Response("Presupuesto ya aprobado o cerrado, no se puede editar.", status=status.HTTP_400_BAD_REQUEST)
                return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pro_pk, pre_pk, format=None):  # este verbo lo usa el vendedor para editar campos presupuestos
        try:

            if(request.data['estatus'] == "Cerrado"):

                presupuesto = Presupuesto.objects.get(codigo=pre_pk)
                if (presupuesto.estatus != "Aprobado"):
                    return Response("Solo se pueden cerrar los presupuestos aprobados.", status=status.HTTP_400_BAD_REQUEST)

                etapas = Etapa.objects.filter(codigo_pro=pro_pk)
                noCulminadaFacturada = False
                for etapa in etapas:
                    if (etapa.estatus != "Culminado" or etapa.facturada is False):
                        noCulminadaFacturada = True
                if (noCulminadaFacturada is True):
                    return Response("No se puede cerrar el presupuesto hay etapas que no han culminado o no se han facturado.", status=status.HTTP_400_BAD_REQUEST)

                presupuesto.estatus = "Cerrado"
                presupuesto.save()
                data = {}
                data['data'] = request.data
                data['msg'] = "Presupuesto Cerrado exitosamente!"
                return Response(data, status=status.HTTP_200_OK)

            proyecto = Proyecto.objects.get(codigo=pro_pk)
            if (proyecto.estatus == "Rechazado" or proyecto.estatus == "Culminado"):
                return Response("El estado del proyecto no permite editar el presupuesto.", status=status.HTTP_400_BAD_REQUEST)

            presupuesto = Presupuesto.objects.get(codigo=pre_pk)
            if(presupuesto.estatus != "Aprobado" and presupuesto.estatus != "Cerrado"):
                s_presupuesto = PresupuestoSerializer(presupuesto, data=request.data)
                if (s_presupuesto.is_valid(raise_exception=True)):
                    s_presupuesto.save()
                    msg = "Presupuesto " + s_presupuesto.validated_data['codigo'] + " editado exitosamente!"
                    data = {}
                    data['data'] = s_presupuesto.data
                    data['msg'] = msg
                    return Response(data, status=status.HTTP_200_OK)
            else:
                return Response("Presupuesto " + presupuesto.codigo + " ya aprobado o cerrado, no se puede editar", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class Tecnicos(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        tecnicos = Trabajador.objects.filter(cargo='t').order_by('ci')
        serializer = TrabajadorSerializer(tecnicos, many=True)
        for tecnico in serializer.data:
            tecnico['nombre'] = tecnico['nombre1'] +" "+tecnico['nombre2'] +" "+tecnico['apellido1'] +" "+tecnico['apellido2']
            proyectos = Proyecto_tecnico.objects.filter(ci_tecnico=tecnico['ci'])
            tecnico['proyectos'] = []
            for proyecto in proyectos:
                aux = {}
                aux['codigo_pro'] = proyecto.codigo_pro.codigo
                aux['nombre_pro'] = proyecto.codigo_pro.nombre
                tecnico['proyectos'].append(aux)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProyectoTecnicos(APIView):
    permission_classes = [IsAuthenticated, esCoordinador]


    def get(self, request, pk, format=None):
        aux={}
        aux['tecnicos'] = []
        ta = Proyecto_tecnico.objects.filter(codigo_pro=pk)
        tt = Trabajador.objects.filter(cargo='t')

        for tecnico in tt:
            aux_2= {}
            aux_2['ci'] = tecnico.ci
            aux_2['nombre'] = tecnico.nombre1 + " " + tecnico.nombre2 + " " + tecnico.apellido1 + " " + tecnico.apellido2            
            aux_2['tlf'] = tecnico.tlf
            aux_2['correo'] = tecnico.correo
            aux['tecnicos'].append(aux_2)

        for tecnico in aux['tecnicos']:
            flag = False
            for tecnicos_asociado in ta:
                if (tecnicos_asociado.ci_tecnico.ci == tecnico['ci']):
                    flag = True
            
            tecnico['mostrar_asociado'] = flag

        return Response(aux['tecnicos'], status=status.HTTP_200_OK)


    def post(self, request, pk, format=None):
        try:
            with transaction.atomic():
                # print(request.data)
                proyecto = Proyecto.objects.get(codigo=pk)

                if (proyecto.estatus!="Ejecucion" and proyecto.estatus!="Culminado" and proyecto.estatus!="Rechazado"):
                    Proyecto_tecnico.objects.filter(codigo_pro=pk).delete()
                    for tecnico in request.data:
                        t = Trabajador.objects.get(ci=tecnico['ci'])
                        Proyecto_tecnico.objects.create(ci_tecnico=t, codigo_pro=proyecto)
                    data = {}
                    data['data'] = request.data
                    data['msg'] = "Tecnicos guardados exitosamente."
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    return Response("No se pueden guardar los tecnicos debido al estado del proyecto.", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class ProcesarSolicitud(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, format=None):
        with transaction.atomic():
            sol = Solicitud.objects.get(codigo=request.data['solicitud']['codigo'])
            if (sol.estatus != "Nueva"):
                return Response("Solicitud ya estaba procesada", status=status.HTTP_400_BAD_REQUEST)
            solicitud = SolicitudSerializer(sol, data=request.data['solicitud'])
            if (solicitud.is_valid()):
                solicitud.save()
            else:
                print(solicitud.errors)

            proyecto = ProyectoSerializer(data=request.data['proyecto'])
            if (proyecto.is_valid()):
                proyecto.save()
                proyecto_tecnico = ProyectoTecnicoSerializer(data=request. data['proyecto_tecnico'])
                if (proyecto_tecnico.is_valid()):
                    proyecto_tecnico.save()
                else:
                    print(proyecto_tecnico.errors)
            else:
                print(proyecto.errors)
            data = {}
            data['data'] = proyecto.data
            data['msg'] = "Solicitud procesada exitosamente."
            return Response(data, status=status.HTTP_200_OK)
        return Response("Solicitud no pudo ser procesada", status=status.HTTP_400_BAD_REQUEST)


class ServicioList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Servicio.objects.all().order_by('codigo')
    serializer_class = ServicioSerializer


class ServicioDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Servicio.objects.all().order_by('codigo')
    serializer_class = ServicioSerializer


class ProyectoCoordinador(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk, format=None):
        try:
            proyectos = Proyecto.objects.filter(ci_coord=pk).order_by('codigo')
            serializer = ProyectoSerializer(proyectos, many=True)
            for proyecto in serializer.data:
                solicitud = Solicitud.objects.get(codigo=proyecto['codigo_s'])
                serializerS = SolicitudSerializerAll(solicitud)
                proyecto['rif_c'] = serializerS.data['rif_c']
                cliente = Cliente.objects.get(rif=proyecto['rif_c'])
                serializerC = ClienteSerializer(cliente)
                proyecto['nombre_c'] = serializerC.data['nombre']
                try:
                    reporte_inicial = Reporte_inicial.objects.get(codigo=proyecto['codigo_ri'])
                    serializerRI = ReporteInicialSerializer(reporte_inicial)
                    proyecto['reporte_inicial'] = serializerRI.data
                except Reporte_inicial.DoesNotExist:
                    proyecto['reporte_inicial'] = None
        except Cliente.DoesNotExist:
            return Response("Error relacionando proyecto con cliente", status=status.HTTP_400_BAD_REQUEST)
        except Solicitud.DoesNotExist:
                return Response("Error relacionando proyecto con solicitud", status=status.HTTP_400_BAD_REQUEST)
        except Proyecto.DoesNotExist:
           return Response("No existe proyecto con esas caracteristicas", status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
