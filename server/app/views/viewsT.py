from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from app.permissions import esTecnicoOsoloLectura
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app.serializers.serializersT import ReporteInicialSerializer
from app.models import Proyecto


def viewsTecnico(arg):
    pass


class ReporteInicial(APIView):
    permission_classes = [IsAuthenticated,esTecnicoOsoloLectura] #,esTecnico]

    def post(self,request, pk, format=None):
        proyecto = Proyecto.objects.get(codigo=pk)
        if (proyecto.codigo_ri == None):
            reporte_inicial = ReporteInicialSerializer(data=request.data)
            if (reporte_inicial.is_valid()):
                ri = reporte_inicial.save()
                proyecto.codigo_ri = ri
                proyecto.save()
        else:
            return Response("Este proyecto ya tiene un reporte inicial.", status=status.HTTP_400_BAD_REQUEST)
        return Response(reporte_inicial.data, status=status.HTTP_200_OK)
