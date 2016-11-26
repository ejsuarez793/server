from rest_framework import serializers

from app.models import Solicitud, Proyecto, Proyecto_tecnico, Servicio, Cliente, Reporte_inicial


def CoordinadorSerializers(arg):
    pass


class SolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = ('codigo', 'f_vis','estatus')


class SolicitudSerializerAll(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = '__all__'


class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = '__all__'


class ProyectoTecnicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto_tecnico
        fields = '__all__'


class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = '__all__'


class ReporteInicialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reporte_inicial
        fields = '__all__'
