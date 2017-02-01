from rest_framework import serializers

# modelos a importar
from app.models import Cliente, Solicitud, Proyecto, Presupuesto, Causa_rechazo, Encuesta, Pregunta, Factura


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


class EncuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Encuesta
        fields = '__all__'


class PreguntaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pregunta
        fields = '__all__'


class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = '__all__'
