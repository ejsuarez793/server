from rest_framework import serializers

# modelos a importar
from app.models import Cliente


def VendedorSerializers(arg):
    pass


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'
