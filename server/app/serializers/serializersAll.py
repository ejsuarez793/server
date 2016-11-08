from rest_framework import serializers
from django.contrib.auth.models import User
from app.models import Trabajador


def TodosSerializers(arg):
    pass


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = fields = ('id', 'username', 'password', 'email')
        write_only_fields = ('password',)


class TrabajadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trabajador
        fields = '__all__'


"""class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()
    ci = serializers.CharField(max_length=10)
    nombre1 = serializers.CharField(max_length=15)
    nombre2 = serializers.CharField(max_length=15)
    apellido1 = serializers.CharField(max_length=15)
    apellido2 = serializers.CharField(max_length=15)
    tlf = serializers.CharField(max_length=15)
    correo = serializers.EmailField()
    dire = serializers.CharField(max_length=50)
    cargo = serializers.CharField(max_length=1)"""
