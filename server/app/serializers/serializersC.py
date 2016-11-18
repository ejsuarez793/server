from rest_framework import serializers

from app.models import Solicitud, Proyecto,Proyecto_tecnico


def CoordinadorSerializers(arg):
    pass


class SolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = ('codigo','f_vis')


class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = '__all__'


class ProyectoTecnicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto_tecnico
        fields = '__all__'
