from app.models import Cliente, Solicitud
from app.serializers.serializersV import ClienteSerializer, SolicitudSerializer, Causa_rechazoSerializer
from rest_framework import generics
from rest_framework.views import APIView

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)

from rest_framework.response import Response
from rest_framework import status
from django.db import transaction


from app.permissions import esVendedor
from app.serializers.serializersV import ProyectoEstatusSerializer, PresupuestoSerializer
from app.models import Proyecto, Presupuesto, Material_presupuesto, Servicio_presupuesto


def viewsVendedor(arg):
    pass


class ClienteList(generics.ListCreateAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class ClienteDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class SolicitudList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer


class ProyectoProcesarEstatus(APIView):
    permission_classes = [esVendedor]

    def patch(self, request, pk, format=None):
        try:
            with transaction.atomic():
                proyecto = Proyecto.objects.get(codigo=pk)
                if(proyecto.estatus != "Aprobado"):
                    s_proyecto = ProyectoEstatusSerializer(proyecto, data=request.data)
                    if(s_proyecto.is_valid(raise_exception=True)):
                        presupuestos = Presupuesto.objects.filter(codigo_pro=s_proyecto.validated_data['codigo'])
                        s_presupuestos = PresupuestoSerializer(presupuestos, many=True)
                        if(s_proyecto.validated_data['estatus']=="Aprobado"):
                            flag = False
                            for presupuesto in s_presupuestos.data:
                                if (presupuesto['estatus']!="Aprobado"):
                                    Material_presupuesto.objects.filter(codigo_pre=presupuesto['codigo']).delete()
                                    Servicio_presupuesto.objects.filter(codigo_pre=presupuesto['codigo']).delete()
                                    Presupuesto.objects.get(codigo=presupuesto['codigo']).delete()

                        elif(s_proyecto.validated_data['estatus']=="Rechazado"):
                            flag = False
                            for presupuesto in s_presupuestos.data:
                                if (presupuesto['estatus']!="Rechazado"):
                                    flag = True
                            if (flag==True):
                                return Response("Proyecto tiene un presupuesto que no ha sido rechazado",status=status.HTTP_400_BAD_REQUEST)
                        s_proyecto.save()
                return Response(s_proyecto.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class ProyectoCausaRechazo(APIView):
    permission_classes = [esVendedor]

    def post(self, request, pk, format=None):
        try:
            s_causa_rechazo = Causa_rechazoSerializer(data=request.data)
            if(s_causa_rechazo.is_valid(raise_exception=True)):
                s_causa_rechazo.save()
                return Response(s_causa_rechazo.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)