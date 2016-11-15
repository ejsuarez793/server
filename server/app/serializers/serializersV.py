from rest_framework import serializers

# modelos a importar
from app.models import Cliente,Solicitud


def VendedorSerializers(arg):
    pass


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'


class SolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = '__all__'