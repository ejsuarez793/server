from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from app.permissions import esTecnico, esCoordinador
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from app.serializers.serializersT import ReporteInicialSerializer, ReporteDetalleSerializer, ReporteSerializer
from app.models import Proyecto, Etapa, Reporte, Movimiento, Material, Material_movimiento, Etapa_tecnico_movimiento, Trabajador, Proyecto_tecnico


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


class ProyectoTecnico(APIView):
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


class ReporteInicial(APIView):
    permission_classes = [IsAuthenticated, esTecnico] #,esTecnico]

    def post(self, request, pk, format=None):
        proyecto = Proyecto.objects.get(codigo=pk)
        if (proyecto.codigo_ri is None):
            reporte_inicial = ReporteInicialSerializer(data=request.data)
            if (reporte_inicial.is_valid()):
                ri = reporte_inicial.save()
                proyecto.codigo_ri = ri
                proyecto.save()
        else:
            return Response("Este proyecto ya tiene un reporte inicial.", status=status.HTTP_400_BAD_REQUEST)
        return Response(reporte_inicial.data, status=status.HTTP_200_OK)


class ReporteDetalle(APIView):
    permission_classes = [IsAuthenticated, esTecnico]

    def post(self, request, pk_p, pk_e, format=None):
        try:
            etapa = Etapa.objects.get(codigo=pk_e)
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


class ReporteDetail(APIView):
    permission_classes = [IsAuthenticated, esTecnico]

    def post(self, request, pk_p, pk_e, format=None):
        try:
            reporte = ReporteSerializer(data=request.data)
            if (reporte.is_valid(raise_exception=True)):
                reporte.save()
                data = {}
                data['data'] = reporte.data
                data['msg'] = "Reporte enviado exitosamente!"
                return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk_p, pk_e, format=None):
        try:
            with transaction.atomic():
                for codigo in request.data['codigos']:
                    reporte = Reporte.objects.get(codigo=codigo)
                    reporte.leido=True
                    reporte.save()
                data = {}
                data['data'] = request.data
                data['msg'] = "Reportes marcados como leidos exitosamente!"
                return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

# permite crear una solicitud de material para una etapa
class SolicitudMaterialDetail(APIView):
    permission_classes = [IsAuthenticated, esTecnico]

    def post(self, request, pk_p, pk_e, format=None):
        try:
            with transaction.atomic():
                movimiento = Movimiento.objects.create(tipo="Egreso")
                tecnico = Trabajador.objects.get(ci=request.data['otros']['ci_tecnico'])

                #print(movimiento.codigo)
                for material in request.data['materiales']:
                    print(material)
                    m = Material.objects.get(codigo=material['codigo_mat'])
                    Material_movimiento.objects.create(codigo_mov=movimiento, codigo_mat=m, cantidad=material['cant']);

                etapa = Etapa.objects.get(codigo=request.data['otros']['codigo_eta'])
                Etapa_tecnico_movimiento.objects.create(ci_tecnico=tecnico, codigo_eta=etapa, codigo_mov=movimiento)
                data = {}
                data['data'] = request.data
                data['msg'] = "Solicitud enviada exitosamente!"
                return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)