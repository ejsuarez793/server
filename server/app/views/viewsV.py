from app.models import Cliente
from app.serializers.serializersV import ClienteSerializer
from rest_framework import generics


def viewsVendedor(arg):
    pass


class ClienteList(generics.ListCreateAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class ClienteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
