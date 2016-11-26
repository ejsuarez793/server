from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from app.permissions import esAlmacenista
from app.serializers.serializersA import MaterialSerializer, EquipoSerializer
from app.models import Material, Equipo


def viewsAlmacenista(arg):
    pass


class MaterialList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, esAlmacenista]

    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class EquipoList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, esAlmacenista]

    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer

class EquipoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, esAlmacenista]

    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer