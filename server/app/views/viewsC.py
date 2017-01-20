#from django.contrib.auth.models import User
from app.models import Trabajador, Solicitud, Servicio,Proyecto, Etapa, Actividad, Reporte_detalle, Reporte, Causa_rechazo, Encuesta, Pregunta, Movimiento, Etapa_tecnico_movimiento, Material_movimiento, Material, Cliente,Reporte_inicial,Presupuesto, Servicio_presupuesto, Material_presupuesto
from app.serializers.serializersAll import TrabajadorSerializer
from app.serializers.serializersV import ClienteSerializer
from app.serializers.serializersC import ProyectoSerializer, ProyectoSerializerPG, EtapaSerializer, ActividadSerializer, ReporteDetalleSerializer, ReporteSerializer, PresupuestoSerializer, Causa_rechazoSerializer, PreguntaSerializer, EncuestaSerializer, MaterialSerializer, Servicio_presupuestoSerializer, Material_presupuestoSerializer, SolicitudSerializer, SolicitudSerializerAll, ProyectoTecnicoSerializer, ServicioSerializer, ReporteInicialSerializer
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
        proyectos = Proyecto.objects.all()
        s_proyectos = ProyectoSerializer(proyectos, many=True)
        for proyecto in s_proyectos.data:
            solicitud = Solicitud.objects.get(codigo=proyecto['codigo_s'])
            s_solicitud = SolicitudSerializerAll(solicitud)
            cliente = Cliente.objects.get(rif=s_solicitud.data['rif_c'])
            s_cliente = ClienteSerializer(cliente)
            proyecto['nombre_c'] = s_cliente.data['nombre']
        return Response(s_proyectos.data, status=status.HTTP_200_OK)


class ProyectoDetail(APIView):
    permission_classes = [IsAuthenticated, esCoordinador]

    def get(self, request, pk, format=None):
        proyecto = Proyecto.objects.get(codigo=pk)
        s_proyecto = ProyectoSerializer(proyecto)

        solicitud = Solicitud.objects.get(codigo=s_proyecto.data['codigo_s'])
        s_solicitud = SolicitudSerializerAll(solicitud)

        cliente = Cliente.objects.get(rif=s_solicitud.data['rif_c'])
        s_cliente = ClienteSerializer(cliente)

        presupuestos = Presupuesto.objects.filter(codigo_pro=s_proyecto.data['codigo'])
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
                material['desc'] = s_mat.data['desc']

        proyecto = s_proyecto.data
        proyecto['cliente'] = s_cliente.data
        proyecto['presupuestos'] = s_presupuestos.data

        try:
            causa_rechazo = Causa_rechazo.objects.get(codigo_pro=s_proyecto.data['codigo'])
            s_causa_rechazo = Causa_rechazoSerializer(causa_rechazo)
            proyecto['causa_rechazo'] = s_causa_rechazo.data
        except Causa_rechazo.DoesNotExist:
            proyecto['causa_rechazo'] = None


        try:
            etapas = Etapa.objects.filter(codigo_pro=s_proyecto.data['codigo'])
            s_etapas = EtapaSerializer(etapas, many=True)
            try:
                for etapa in s_etapas.data: 
                    reporte_detalle = Reporte_detalle.objects.get(codigo=etapa['codigo_rd'])
                    s_reporte_detalle = ReporteDetalleSerializer(reporte_detalle)
                    etapa['reporte_detalle'] = s_reporte_detalle.data

                    reportes = Reporte.objects.filter(codigo_eta=etapa['codigo']).order_by('fecha')
                    s_reportes = ReporteSerializer(reportes, many=True)
                    etapa['reportes'] = s_reportes.data

                    actividades = Actividad.objects.filter(codigo_eta=etapa['codigo'])
                    s_actividades = ActividadSerializer(actividades, many=True)
                    etapa['actividades'] = s_actividades.data

                    etms = Etapa_tecnico_movimiento.objects.filter(codigo_eta=etapa['codigo']).order_by('codigo')
                    solicitudes=[]
                    for etm in etms:
                        if (etm.codigo_mov.tipo=="Egreso"):
                            aux = {}
                            aux['codigo'] = etm.codigo_mov.codigo
                            aux['nombre_t'] = etm.ci_tecnico.nombre1 + " " +etm.ci_tecnico.apellido1
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
            s_preguntas = PreguntaSerializer(preguntas,many=True)
            proyecto['encuesta'] = s_encuesta.data
            proyecto['encuesta']['preguntas'] = s_preguntas.data
        except (Causa_rechazo.DoesNotExist, Encuesta.DoesNotExist):
            proyecto['encuesta'] = None

        return Response(proyecto, status=status.HTTP_200_OK)

    def patch(self, request, pk, format=None):
        try:
            proyecto = Proyecto.objects.get(codigo=pk)
            s_proyecto = ProyectoSerializerPG(proyecto, data=request.data)
            if (s_proyecto.is_valid(raise_exception=True)):
                s_proyecto.save()
                data = {}
                data['data'] = s_proyecto.data
                data['msg'] = "Proyecto editado exitosamente!"
                return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class ProyectoEtapa(APIView):
    permissions_classes = [IsAuthenticated, esCoordinador]

    def post(self, request, pk, format=None):
        try:
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

     def patch(self, request, pk_p,pk_e, format=None):
        try:
            etapa = Etapa.objects.get(codigo=pk_e)
            s_etapa = EtapaSerializer(etapa,data=request.data)
            if(s_etapa.is_valid(raise_exception=True)):
                s_etapa.save()
                data = {}
                data['data'] = s_etapa.data
                data['msg'] = "Etapa editada exitosamente!"
                return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class ActividadDetail(APIView):
    permissions_classes = [IsAuthenticated, esCoordinador]

    def post(self, request, pk_p,pk_e, format=None):
        try:
            print(request.data)
            s_actividad = ActividadSerializer(data=request.data, many=True)
            if (s_actividad.is_valid(raise_exception=True)):
                s_actividad.save()
                data = {}
                data['data'] = s_actividad.data
                data['msg'] = "Actividades definidas exitosamente!"
                return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class ProyectoMaterialDesglose(APIView):
    permissions_classes = [IsAuthenticated] ##aqui falta poner esCoordinadoroALmacenista o dejarlo asi

    def get(self, request, pk, format=None):
        data_desglose = {}
        data_presupuestos = []
        data_egresados = []
        data_retornados = []
        aux = {}

        #primero buscamos los materiales que estan en los presupuestos arpobados del proyecto
        presupuestos = Presupuesto.objects.filter(codigo_pro=pk)
        for presupuesto in presupuestos:
            if (presupuesto.estatus == "Aprobado"):
                materiales_presupuesto = Material_presupuesto.objects.filter(codigo_pre=presupuesto.codigo)
                for material_presupuesto in materiales_presupuesto:
                    aux = {}
                    aux['codigo_pre'] = presupuesto.codigo
                    aux['codigo_mat'] = material_presupuesto.codigo_mat.codigo
                    aux['nombre'] = material_presupuesto.codigo_mat.nombre
                    aux['desc'] = material_presupuesto.codigo_mat.desc
                    aux['serial'] = material_presupuesto.codigo_mat.serial
                    aux['cant'] = material_presupuesto.cantidad
                    data_presupuestos.append(aux)

        """print("presupuestos materiales")
        print(data_presupuestos)"""

        #luego buscamos los materiales que han salido a una etapa del proyecto
        aux = {}
        etapas = Etapa.objects.filter(codigo_pro=pk)
        for etapa in etapas:
            etms = Etapa_tecnico_movimiento.objects.filter(codigo_eta=etapa.codigo)
            for etm in etms:
                if (etm.codigo_mov.completado==True):
                    mm = Material_movimiento.objects.get(codigo_mov=etm.codigo_mov.codigo)
                    aux = {}
                    aux['codigo_mov'] = etm.codigo_mov.codigo
                    aux['tipo_mov'] = etm.codigo_mov.tipo
                    aux['codigo_mat'] = mm.codigo_mat.codigo
                    aux['nombre'] = mm.codigo_mat.nombre
                    aux['desc'] = mm.codigo_mat.desc
                    aux['serial'] = mm.codigo_mat.serial
                    aux['cant'] = mm.cantidad
                    aux['codigo_eta'] = etapa.codigo
                    aux['nombre_eta'] = etapa.nombre
                    if (etm.codigo_mov.tipo == "Egreso"):
                        data_egresados.append(aux)
                    elif(etm.codigo_mov.tipo == "Retorno"):
                        data_retornados.append(aux)
        """print("materiales egresados")
        print(data_egresados)
        print("materiales retornados")
        print(data_retornados)"""
        data_desglose['presupuestos'] = data_presupuestos
        data_desglose['egresados'] = data_egresados
        data_desglose['retornados'] = data_retornados
        #print(data_desglose)
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
        return Response(data,status=status.HTTP_200_OK)


class PresupuestoList(APIView):
    permission_classes = [IsAuthenticated, esCoordinador]

    def post(self, request, pk, format=None):
        try:
            with transaction.atomic():
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

    def patch(self, request, pro_pk, pre_pk, format=None):# este verbo lo usa el coordinador para editar los mat y serv del presupuesto

        try:
            with transaction.atomic():
                presupuesto = Presupuesto.objects.get(codigo=pre_pk)
                if(presupuesto.estatus != "Aprobado"):
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
                    data = {}
                    data['data'] = request.data
                    data['msg'] = "Presupuesto ya aprobado no se puede editar."
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
                return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pro_pk, pre_pk, format=None):#este verbo lo usa el vendedor para editar campos presupuestos
        try:
            presupuesto = Presupuesto.objects.get(codigo=pre_pk)
            if(presupuesto.estatus != "Aprobado"):
                s_presupuesto = PresupuestoSerializer(presupuesto, data=request.data)
                if (s_presupuesto.is_valid(raise_exception=True)):
                    s_presupuesto.save()
                    msg = "Presupuesto " +s_presupuesto.validated_data['codigo']+" editado exitosamente!"
                    data = {}
                    data['data'] = s_presupuesto.data
                    data['msg'] = msg
                    return Response(data, status=status.HTTP_200_OK)
            else:
                return Response("Presupuesto " + presupuesto.codigo+" ya aprobado, no se puede editar", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class Tecnicos(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        tecnicos = Trabajador.objects.get(cargo='t')
        serializer = TrabajadorSerializer(tecnicos)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProcesarSolicitud(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, format=None):
        with transaction.atomic():
            sol = Solicitud.objects.get(codigo=request.data['solicitud']['codigo'])
            if (sol.estatus != "n"):
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
            return Response("Solicitud Procesada", status=status.HTTP_200_OK)
        return Response("Solicitud No pudo ser procesada", status=status.HTTP_400_BAD_REQUEST)


class ServicioList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer


class ServicioDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer


class ProyectoCoordinador(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk, format=None):
        try:
            proyectos = Proyecto.objects.filter(ci_coord=pk)
            serializer = ProyectoSerializer(proyectos, many=True)
            for proyecto in serializer.data:
                solicitud = Solicitud.objects.get(codigo=proyecto['codigo_s'])
                serializerS = SolicitudSerializerAll(solicitud)
                proyecto['rif_c'] = serializerS.data['rif_c']
                cliente = Cliente.objects.get(rif=proyecto['rif_c'])
                serializerC = ClienteSerializer(cliente)
                proyecto['nombre_c'] = serializerC.data['nombre']
                reporte_inicial = Reporte_inicial.objects.get(codigo=proyecto['codigo_ri'])
                serializerRI = ReporteInicialSerializer(reporte_inicial)
                proyecto['reporte_inicial'] = serializerRI.data
        except Cliente.DoesNotExist:
            return Response("Error relacionando proyecto con cliente", status=status.HTTP_400_BAD_REQUEST)
        except Solicitud.DoesNotExist:
                return Response("Error relacionando proyecto con solicitud", status=status.HTTP_400_BAD_REQUEST)
        except Proyecto.DoesNotExist:
           return Response("No existe proyecto con esas caracteristicas", status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
