from rest_framework import serializers

from app.models import Solicitud, Proyecto, Etapa, Actividad, Reporte_detalle, Reporte, Proyecto_tecnico, Servicio, Material, Reporte_inicial, Presupuesto, Servicio_presupuesto, Material_presupuesto, Causa_rechazo, Encuesta, Pregunta


def CoordinadorSerializers(arg):
    pass


class SolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = ('codigo', 'f_vis', 'estatus')


class SolicitudSerializerAll(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = '__all__'


class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = '__all__'


class ProyectoSerializerPG(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = ('nombre', 'desc', 'f_est', 'ubicacion')


class EtapaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etapa
        fields = '__all__'


class ActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = '__all__'


class ReporteDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reporte_detalle
        fields = '__all__'


class ReporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reporte
        fields = '__all__'


class ProyectoTecnicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto_tecnico
        fields = '__all__'


class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'


class ReporteInicialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reporte_inicial
        fields = '__all__'


class PresupuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presupuesto
        fields = '__all__'


class Servicio_presupuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio_presupuesto
        fields = '__all__'


class Material_presupuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material_presupuesto
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
