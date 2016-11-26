from rest_framework import serializers

from app.models import Material, Equipo


def AlmacenistaSerializers(arg):
    pass


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'


class EquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipo
        fields = '__all__'
