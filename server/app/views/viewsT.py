from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from app.permissions import esTecnicoOsoloLectura, esCoordinador
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from app.serializers.serializersT import ReporteInicialSerializer, ReporteDetalleSerializer, ReporteSerializer
from app.models import Proyecto, Etapa, Reporte


def viewsTecnico(arg):
    pass


class ReporteInicial(APIView):
    permission_classes = [IsAuthenticated, esTecnicoOsoloLectura] #,esTecnico]

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
    permission_classes = [IsAuthenticated, esCoordinador]

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
    permission_classes = [IsAuthenticated, esCoordinador]

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
