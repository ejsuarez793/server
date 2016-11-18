from django.contrib.auth.models import User
from app.models import Trabajador,Solicitud
from app.serializers.serializersAll import TrabajadorSerializer
from app.serializers.serializersC import ProyectoSerializer, SolicitudSerializer, ProyectoTecnicoSerializer
from django.db import transaction
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


def viewsCoordinador(arg):
    pass


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
            solicitud = SolicitudSerializer(sol,data=request.data['solicitud'])
            if (solicitud.is_valid()):
                print("solicitud valida")
                solicitud.save()
            else:
                print(solicitud.errors)

            proyecto = ProyectoSerializer(data=request.data['proyecto'])
            if (proyecto.is_valid()):
                print("proyecto valido")
                proyecto.save()
                proyecto_tecnico = ProyectoTecnicoSerializer(data=request.data['proyecto_tecnico'])
                if (proyecto_tecnico.is_valid()):
                    print("proyecto tecnico valido")
                    proyecto_tecnico.save()
                else:
                    print(proyecto_tecnico.errors)
            else:
                print(proyecto.errors)


            return Response("epale todo bien", status=status.HTTP_200_OK)
