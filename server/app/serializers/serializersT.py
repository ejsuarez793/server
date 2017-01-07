from rest_framework import serializers

from app.models import Reporte_inicial, Reporte_detalle, Reporte

def TecnicoSerializers(arg):
    pass

class ReporteInicialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reporte_inicial
        fields = '__all__'


class ReporteDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reporte_detalle
        fields = '__all__'


class ReporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reporte
        fields = '__all__'
