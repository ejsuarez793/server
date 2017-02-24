from rest_framework import serializers

from app.models import Material, Proveedor, Material_proveedor #,Equipo


def AlmacenistaSerializers(arg):
    pass




"""class EquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipo
        fields = '__all__'"""


class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'


class MaterialProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material_proveedor
        fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Material
        fields = '__all__'
