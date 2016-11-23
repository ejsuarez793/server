from django.contrib.auth.models import User
from app.models import Trabajador, Solicitud, Servicio,Proyecto, Cliente
from app.serializers.serializersAll import TrabajadorSerializer
from app.serializers.serializersV import ClienteSerializer
from app.serializers.serializersC import ProyectoSerializer, SolicitudSerializer, SolicitudSerializerAll, ProyectoTecnicoSerializer, ServicioSerializer
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
from rest_framework import generics



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
            print(sol.estatus)
            if (sol.estatus == "p"):
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
    
    def get(self, request, format=None):
        try:
            proyectos = Proyecto.objects.filter(ci_coord=self.request.query_params.get('ci_coord'))
            serializer = ProyectoSerializer(proyectos, many=True)
            for proyecto in serializer.data:
                try:
                    solicitud = Solicitud.objects.get(codigo=proyecto['codigo_s'])
                    serializerS = SolicitudSerializerAll(solicitud)
                    proyecto['rif_c'] = serializerS.data['rif_c']
                    try:
                        cliente = Cliente.objects.get(rif=proyecto['rif_c'])
                        serializerC = ClienteSerializer(cliente)
                        proyecto['nombre_c'] = serializerC.data['nombre']
                    except Cliente.DoesNotExist:
                        return Response("Error relacionando proyecto con cliente", status=status.HTTP_400_BAD_REQUEST)
                except Solicitud.DoesNotExist:
                    return Response("Error relacionando proyecto con solicitud", status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Proyecto.DoesNotExist:
           return Response("No existe proyecto con esas caracteristicas", status=status.HTTP_400_BAD_REQUEST)
        
