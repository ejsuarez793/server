from app.models import Cliente, Solicitud
from app.serializers.serializersV import ClienteSerializer, SolicitudSerializer
from rest_framework import generics

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)


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
