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
import json


from app.permissions import esVendedor
from app.serializers.serializersV import ProyectoEstatusSerializer, PresupuestoSerializer, EncuestaSerializer, PreguntaSerializer
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


"""class SolicitudList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer"""

class SolicitudList(APIView):
    permission_classes = [IsAuthenticated, esVendedor]

    def get(self, request, format=None):
        try:
            solicitudes = Solicitud.objects.all()
            data = []
            for solicitud in solicitudes:
                aux={}
                aux['codigo'] = solicitud.codigo
                aux['rif_c'] = solicitud.rif_c.rif
                aux['disp'] = solicitud.disp
                aux['referido_p'] = solicitud.referido_p
                aux['desc'] = solicitud.desc
                aux['ubicacion'] = solicitud.ubicacion
                aux['estatus'] = solicitud.estatus
                aux['nombre_cc'] = solicitud.nombre_cc
                aux['tlf_cc'] = solicitud.tlf_cc
                aux['correo_cc'] = solicitud.correo_cc
                aux['cargo_cc'] = solicitud.cargo_cc
                aux['f_sol'] = solicitud.f_sol
                aux['f_vis'] = solicitud.f_vis
                aux['nombre_cliente'] = solicitud.rif_c.nombre
                aux['tlf1'] = solicitud.rif_c.tlf1
                aux['tlf2'] = solicitud.rif_c.tlf2
                aux['fax'] = solicitud.rif_c.fax
                data.append(aux)
            return Response(data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)





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
                                if (presupuesto['estatus']=="Preventa"):
                                    return Response("Proyecto tiene un presupuesto que sigue en preventa",status=status.HTTP_400_BAD_REQUEST)
                            for presupuesto in s_presupuestos.data:
                                if (presupuesto['estatus']=="Rechazado"):
                                    print("p")
                                    #Material_presupuesto.objects.filter(codigo_pre=presupuesto['codigo']).delete()
                                    #Servicio_presupuesto.objects.filter(codigo_pre=presupuesto['codigo']).delete()
                                    #Presupuesto.objects.get(codigo=presupuesto['codigo']).delete()

                        elif(s_proyecto.validated_data['estatus']=="Rechazado"):
                            flag = False
                            for presupuesto in s_presupuestos.data:
                                if (presupuesto['estatus']!="Rechazado"):
                                    flag = True
                            if (flag==True):
                                return Response("Proyecto tiene un presupuesto que no ha sido rechazado",status=status.HTTP_400_BAD_REQUEST)
                        s_proyecto.save()
                        msg = "Proyecto " +s_proyecto.validated_data['estatus']+" Exitosamente!"
                        data = {}
                        data['data'] = s_proyecto.data
                        data['msg'] = msg
                return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class ProyectoCausaRechazo(APIView):
    permission_classes = [esVendedor]

    def post(self, request, pk, format=None):
        try:
            s_causa_rechazo = Causa_rechazoSerializer(data=request.data)
            if(s_causa_rechazo.is_valid(raise_exception=True)):
                s_causa_rechazo.save()
                msg = "Causa de rechazo almacenada exitosamente!"

                data = {}
                data['data'] = s_causa_rechazo.data
                data['msg'] = msg
                return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class ProyectoEncuesta(APIView):

     def post(self, request, pk, format=None):
        try:
            with transaction.atomic():
                s_encuesta = EncuestaSerializer(data=request.data['encuesta'])
                if (s_encuesta.is_valid(raise_exception=True)):
                    s_encuesta.save()
                    s_preguntas = PreguntaSerializer(data=request.data['preguntas'],many=True)
                    for pregunta in s_preguntas.initial_data:
                        pregunta['codigo_en'] = s_encuesta.data['codigo']
                    if(s_preguntas.is_valid(raise_exception=True)):
                        s_preguntas.save()
                        s_encuesta.data['preguntas'] = s_preguntas.data
                    msg = "Encuesta completada exitosamente!"
                    data = {}
                    data['data'] = s_encuesta.data
                    data['msg'] = msg
                return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)