from rest_framework import serializers

# modelos a importar
from app.models import Cliente, Solicitud, Proyecto, Presupuesto, Causa_rechazo


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


class ProyectoEstatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = ('codigo', 'estatus')


class PresupuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presupuesto
        fields = '__all__'


class Causa_rechazoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Causa_rechazo
        fields = '__all__'