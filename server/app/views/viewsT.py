from rest_framework.permissions import (

    IsAuthenticated,

)
from app.permissions import esTecnico
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from app.serializers.serializersT import ReporteInicialSerializer, ReporteDetalleSerializer, ReporteSerializer
from app.models import Proyecto, Etapa, Presupuesto, Factura, Servicio, Servicio_presupuesto, Material_presupuesto, Actividad, Reporte, Reporte_servicio, Movimiento, Material, Material_movimiento, Etapa_tecnico_movimiento, Trabajador, Proyecto_tecnico


def viewsTecnico(arg):
    pass

class SolicitudTecnico(APIView):
    permission_classes = [IsAuthenticated, esTecnico]

    def get(self, request, ci, format=None):
        proyectos = Proyecto_tecnico.objects.filter(ci_tecnico=ci)
        solicitudes = []
        for proyecto in proyectos:
            if (proyecto.codigo_pro.estatus == "Preventa" and proyecto.codigo_pro.codigo_ri == None):     
                aux = {}
                aux['codigo'] = proyecto.codigo_pro.codigo_s.codigo
                aux['disp'] = proyecto.codigo_pro.codigo_s.disp
                aux['desc'] = proyecto.codigo_pro.codigo_s.desc
                aux['ubicacion'] = proyecto.codigo_pro.codigo_s.ubicacion
                aux['estatus'] = proyecto.codigo_pro.codigo_s.estatus
                aux['nombre_cc'] =  proyecto.codigo_pro.codigo_s.nombre_cc
                aux['cargo_cc'] =  proyecto.codigo_pro.codigo_s.cargo_cc
                aux['tlf_cc'] =  proyecto.codigo_pro.codigo_s.tlf_cc
                aux['correo_cc'] =  proyecto.codigo_pro.codigo_s.correo_cc
                aux['f_sol'] =  proyecto.codigo_pro.codigo_s.f_sol
                aux['nombre_cliente'] = proyecto.codigo_pro.codigo_s.rif_c.nombre
                aux['codigo_pro'] = proyecto.codigo_pro.codigo
                solicitudes.append(aux)
        return Response(solicitudes, status=status.HTTP_200_OK)


class ProyectosTecnico(APIView):
    permission_classes = [IsAuthenticated, esTecnico]

    def get(self, request, ci, format=None):
        proyectos = Proyecto_tecnico.objects.filter(ci_tecnico=ci)
        p = []
        for proyecto in proyectos:
            aux = {}
            aux['codigo'] = proyecto.codigo_pro.codigo
            aux['estatus'] = proyecto.codigo_pro.estatus
            #aux['codigo_ri'] = proyecto.codigo_pro.codigo_ri
            aux['desc'] = proyecto.codigo_pro.desc
            aux['nombre'] = proyecto.codigo_pro.nombre
            aux['ubicacion'] = proyecto.codigo_pro.ubicacion
            p.append(aux)
        return Response(p, status=status.HTTP_200_OK)


class ProyectoTecnico(APIView):
    permission_classes = [IsAuthenticated, esTecnico]

    def get(self, request, pk, format=None):
        proyecto = Proyecto.objects.get(codigo=pk)
        aux={}
        aux['codigo'] = proyecto.codigo
        aux['nombre'] = proyecto.nombre
        aux['desc'] = proyecto.desc
        aux['ubicacion'] = proyecto.ubicacion
        aux['estatus'] = proyecto.estatus
        aux['nombre_coord'] = proyecto.ci_coord.nombre1 + " " +proyecto.ci_coord.apellido1
        aux['etapas'] = []
        etapas = Etapa.objects.filter(codigo_pro=pk).order_by('letra')
        for etapa in etapas:
            aux_2 = {}
            aux_2['codigo_eta'] = etapa.codigo
            aux_2['nombre_eta'] = etapa.nombre
            aux_2['letra_eta'] = etapa.letra
            aux['etapas'].append(aux_2)
        return Response(aux, status=status.HTTP_200_OK)


class EtapaTecnico(APIView):
    permission_classes = [IsAuthenticated, esTecnico]

    def get(self, request, cod_pro, cod_eta, format=None):
        etapa = Etapa.objects.get(codigo=cod_eta)
        eta = {}
        eta['codigo_eta'] = etapa.codigo
        eta['letra_eta'] = etapa.letra
        eta['nombre_eta'] = etapa.nombre
        eta['estatus'] = etapa.estatus
        eta['actividades'] = []
        eta['servicios'] = []
        eta['materiales'] = []

        materiales_disponibles = []
        servicios_disponibles = []
        codigo_presupuesto = ""
        # buscamos las actividades relacionadas a la etapa
        actividades = Actividad.objects.filter(codigo_eta=cod_eta)
        for actividad in actividades:
            aux_act = {}
            aux_act['codigo'] = actividad.codigo
            aux_act['nro'] = actividad.nro
            aux_act['desc'] = actividad.desc
            aux_act['completada'] = actividad.completada
            eta['actividades'].append(aux_act)

        presupuestos = Presupuesto.objects.filter(codigo_pro=cod_pro)
        for presupuesto in presupuestos:
            if (presupuesto.estatus == "Aprobado"):
                codigo_presupuesto = presupuesto.codigo
                break

        # print(codigo_presupuesto)

        # buscamos los servicios presupuestados
        servicios_presupuestos = []
        servicios_pre = Servicio_presupuesto.objects.filter(codigo_pre=codigo_presupuesto)
        for servicio in servicios_pre:
            aux_s = {}
            aux_s['codigo'] = servicio.codigo_ser.codigo
            aux_s['cantidad'] = servicio.cantidad
            aux_s['desc'] = servicio.codigo_ser.desc
            servicios_presupuestos.append(aux_s)
        # print(servicios_presupuestos)

        # buscamos los servicios usados en los reportes
        servicios_reportes = []
        etapas = Etapa.objects.filter(codigo_pro=cod_pro)  # buscamos todas las etapas y sus reportes
        for etapa in etapas:
            considerar = False
            if (etapa.facturada is False):
                considerar = True
            else:
                factura = Factura.objects.get(codigo_eta=etapa.codigo)
                if (factura.codigo_pre.codigo == codigo_presupuesto):
                    considerar = True
            # print(considerar)
            if (considerar is True):
                reportes = Reporte.objects.filter(codigo_eta=etapa.codigo)
                for reporte in reportes:
                    rep_serv = Reporte_servicio.objects.filter(codigo_rep=reporte.codigo)
                    for servicio in rep_serv:
                        print(servicio.codigo_ser.codigo)
                        aux_s = {}
                        aux_s['codigo'] = servicio.codigo_ser.codigo
                        aux_s['cantidad'] = servicio.cantidad
                        aux_s['desc'] = servicio.codigo_ser.desc
                        flag = False  # colocamos esta bandera para saber si ya el servicio fue incluido o no
                        for serv in servicios_reportes:
                            if (serv['codigo'] == aux_s['codigo']):
                                #print(serv['codigo'])
                                serv['cantidad'] += aux_s['cantidad']
                                flag = True  # ya estaba incluido entonces solo sumamos cantidades
                        if (flag is False):  # no estaba incluido y lo aniadimos al array
                            servicios_reportes.append(aux_s)

        # print(servicios_reportes)

        # sacamos los servicios disponibles

        servicios_disponibles = []
        for servicio_presupuesto in servicios_presupuestos:
            flag = False  # colocamos esta bandera para saber si el servicio no ha sido utilizado
            for servicio_reporte in servicios_reportes:
                if (servicio_presupuesto['codigo'] == servicio_reporte['codigo']):
                    aux_s = {}
                    aux_s['codigo'] = servicio_presupuesto['codigo']
                    aux_s['cantidad'] = servicio_presupuesto['cantidad'] - servicio_reporte['cantidad']
                    aux_s['desc'] = servicio_presupuesto['desc']
                    if (aux_s['cantidad'] != 0):
                        servicios_disponibles.append(aux_s)
                    flag = True  # fue utilizado y se restaron las cantidades correspondientes
            if (flag is False):  # no ha sido utilizado y se aniade en su totalidad al array
                servicios_disponibles.append(servicio_presupuesto)

        #print(servicios_disponibles)

        # AHORA BUSCAMOS LOS MATERIALES DISPONIBLES QUE EL TECNICO PUEDE SOLICITAR PARA DICHA ETAPA
        materiales_presupuestos = []
        mat_pre = Material_presupuesto.objects.filter(codigo_pre=codigo_presupuesto)
        for material in mat_pre:
            aux_s = {}
            aux_s['codigo'] = material.codigo_mat.codigo
            aux_s['cantidad'] = material.cantidad
            aux_s['desc'] = material.codigo_mat.nombre + " " + material.codigo_mat.desc + " " + material.codigo_mat.marca
            aux_s['serial'] = material.codigo_mat.serial
            materiales_presupuestos.append(aux_s)

        # print(materiales_presupuestos)
        # print(materiales_presupuestos)

        materiales_usados = []
        for etapa in etapas:
            considerar = False
            if (etapa.facturada is False):
                considerar = True
            else:
                factura = Factura.objects.get(codigo_eta=etapa.codigo)
                if (factura.codigo_pre.codigo == codigo_presupuesto):
                    considerar = True
            # print(considerar)
            if (considerar is True):
                etms = Etapa_tecnico_movimiento.objects.filter(codigo_eta=etapa.codigo)
                for etm in etms:
                    #if (etm.codigo_mov.completado is True):
                    mm = Material_movimiento.objects.filter(codigo_mov=etm.codigo_mov.codigo)
                    for material in mm:
                        aux = {}
                        aux['codigo'] = material.codigo_mat.codigo
                        aux['desc'] = material.codigo_mat.nombre + " " + material.codigo_mat.desc + " " + material.codigo_mat.marca 
                        aux['serial'] = material.codigo_mat.serial
                        aux['cantidad'] = material.cantidad
                        flag = False
                        if (etm.codigo_mov.tipo == "Egreso"):
                            aux['cantidad'] = aux['cantidad'] * 1
                        elif(etm.codigo_mov.tipo == "Retorno"):
                            aux['cantidad'] = aux['cantidad'] * -1
                        for mat in materiales_usados:
                            if (mat['codigo'] == aux['codigo']):
                                mat['cantidad'] += aux['cantidad']
                                flag = True
                        if (flag is False):
                            materiales_usados.append(aux)

        # print(materiales_usados)
        # POR ULTIMO COLOCAMOS EN UN ARRAY LOS MATERIALES DISPONIBLES
        materiales_disponibles = []
        for material_presupuesto in materiales_presupuestos:
            flag = False
            for material_usado in materiales_usados:
                if (material_presupuesto['codigo'] == material_usado['codigo']):
                    aux = {}
                    aux['codigo'] = material_presupuesto['codigo']
                    aux['desc'] = material_presupuesto['desc']
                    aux['serial'] = material_presupuesto['serial']
                    aux['cantidad'] = material_presupuesto['cantidad'] - material_usado['cantidad']
                    flag = True
                    if (aux['cantidad'] != 0):
                        materiales_disponibles.append(aux)
            if (flag is False):
                materiales_disponibles.append(material_presupuesto)

        # print(materiales_disponibles)
        eta['materiales'] = materiales_disponibles
        eta['servicios'] = servicios_disponibles
        return Response(eta, status=status.HTTP_200_OK)


class ReporteInicial(APIView):
    permission_classes = [IsAuthenticated, esTecnico]

    def post(self, request, pk, format=None):
        with transaction.atomic():
            proyecto = Proyecto.objects.get(codigo=pk)
            if (proyecto.codigo_ri is None):
                reporte_inicial = ReporteInicialSerializer(data=request.data)
                if (reporte_inicial.is_valid()):
                    ri = reporte_inicial.save()
                    proyecto.codigo_ri = ri
                    proyecto.save()
                    proyecto.codigo_s.estatus = "Atendida"
                    proyecto.codigo_s.save()
                    data = {}
                    data['data'] = reporte_inicial.data
                    data['msg'] = "Reporte incial completado exitosamente."
            else:
                return Response("Este proyecto ya tiene un reporte inicial.", status=status.HTTP_400_BAD_REQUEST)
            return Response(data, status=status.HTTP_200_OK)


class ActividadTecnico(APIView):
    permission_classes = [IsAuthenticated, esTecnico]

    def patch(self, request, cod_pro, cod_eta, format=None):
        with transaction.atomic():

            proyecto = Proyecto.objects.get(codigo=cod_pro)
            if (proyecto.estatus != "Ejecucion"):
                return Response("El proyecto debe estar en ejecucion para completar las actividades.", status=status.HTTP_400_BAD_REQUEST)

            actividades = request.data
            for actividad in actividades:
                act = Actividad.objects.get(codigo=actividad['codigo'])
                act.completada = True
                act.save()
            data = {}
            data['data'] = request.data
            data['msg'] = "Actividades completadas exitosamente."
            return Response(data, status=status.HTTP_200_OK)


class ReporteDetalle(APIView):
    permission_classes = [IsAuthenticated, esTecnico]

    def post(self, request, pk_p, pk_e, format=None):
        try:

            proyecto = Proyecto.objects.get(codigo=pk_p)
            if (proyecto.estatus != "Ejecucion"):
                return Response("El proyecto debe estar en ejecucion para completar el reporte de detalle.", status=status.HTTP_400_BAD_REQUEST)

            etapa = Etapa.objects.get(codigo=pk_e)
            if (etapa.estatus != "Pendiente"):
                    return Response("Solo las etapas en estado pendiente puede completar el reporte de detalle.", status=status.HTTP_400_BAD_REQUEST)

            if (etapa.codigo_rd is None):
                reporte_detalle = ReporteDetalleSerializer(data=request.data)
                if (reporte_detalle.is_valid(raise_exception=True)):
                    rd = reporte_detalle.save()
                    etapa.codigo_rd = rd
                    etapa.save()
                    data = {}
                    data['data'] = reporte_detalle.data
                    data['msg'] = "Reporte de detalle registrado exitosamente!"
                    return Response(data, status=status.HTTP_200_OK)
            else:
                return Response("Esta etapa ya tiene un reporte de detalle", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class ReporteTecnico(APIView):
    permission_classes = [IsAuthenticated, esTecnico]

    def post(self, request, codigo_pro, codigo_eta, format=None):
        try:
            with transaction.atomic():

                proyecto = Proyecto.objects.get(codigo=codigo_pro)
                if (proyecto.estatus != "Ejecucion"):
                    return Response("El proyecto debe estar en ejecucion para enviar reportes.", status=status.HTTP_400_BAD_REQUEST)

                if (request.data['tipo'] != "Avance" and request.data['servicios']):
                    return Response("Solo los reportes de tipo 'Avance' pueden tener servicios.", status=status.HTTP_400_BAD_REQUEST)
                etapa = Etapa.objects.get(codigo=codigo_eta)
                if (etapa.estatus != "Ejecucion"):
                    return Response("Solo las etapas en ejecucion pueden recibir reportes.", status=status.HTTP_400_BAD_REQUEST)
                reporte = ReporteSerializer(data=request.data)
                if (reporte.is_valid(raise_exception=True)):
                    reporte.save()
                    # print(reporte.data['codigo'])
                    servicios = request.data['servicios']
                    for servicio in servicios:
                        # print(servicio)
                        ser = Servicio.objects.get(codigo=servicio['codigo'])
                        rep = Reporte.objects.get(codigo=reporte.data['codigo'])
                        cant = servicio['cantidad']
                        Reporte_servicio.objects.create(codigo_ser=ser, codigo_rep=rep, cantidad=cant)
                    data = {}
                    data['data'] = reporte.data
                    data['msg'] = "Reporte enviado exitosamente!"
                    return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


# permite crear una solicitud de material para una etapa
class SolicitudMaterial(APIView):
    permission_classes = [IsAuthenticated, esTecnico]

    def post(self, request, codigo_pro, codigo_eta, format=None):
        try:
            with transaction.atomic():

                proyecto = Proyecto.objects.get(codigo=codigo_pro)
                if (proyecto.estatus != "Ejecucion"):
                    return Response("El proyecto debe estar en ejecucion para solicitar materiales.", status=status.HTTP_400_BAD_REQUEST)

                etapa = Etapa.objects.get(codigo=codigo_eta)
                if (etapa.estatus == "Ejecucion"):
                    movimiento = Movimiento.objects.create(tipo="Egreso")
                    tecnico = Trabajador.objects.get(ci=request.data['ci_tecnico'])
                    for material in request.data['materiales']:
                        m = Material.objects.get(codigo=material['codigo'])
                        Material_movimiento.objects.create(codigo_mov=movimiento, codigo_mat=m, cantidad=material['cantidad'])

                    etapa = Etapa.objects.get(codigo=codigo_eta)
                    Etapa_tecnico_movimiento.objects.create(ci_tecnico=tecnico, codigo_eta=etapa, codigo_mov=movimiento)
                    data = {}
                    data['data'] = request.data
                    data['msg'] = "Solicitud enviada exitosamente!"
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    return Response("Etapa debe estar en ejecucion para solicitar materiales.", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)