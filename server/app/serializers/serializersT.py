from rest_framework import serializers

from app.models import Reporte_inicial

def TecnicoSerializers(arg):
    pass

class ReporteInicialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reporte_inicial
        fields = '__all__'