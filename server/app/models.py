from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


#  aqui hay mod dir dire
class Cliente(models.Model):
    opt = (
        ('Ordinario', 'Ordinario'),
        ('Especial', 'Especial'),
        ('Formales', 'Formales'),
    )
    rif = models.CharField(primary_key=True, max_length=15)
    nombre = models.CharField(max_length=75, db_index=True)
    tlf1 = models.CharField(max_length=15)
    tlf2 = models.CharField(max_length=15, blank=True)
    fax = models.CharField(max_length=15, blank=True)
    dire = models.CharField(max_length=200)
    act_eco = models.CharField(max_length=100, blank=True)
    cond_contrib = models.CharField(max_length=10, blank=True, choices=opt)


#  aqui cambio direccio por dire, igua que cargo por 1
class Trabajador(models.Model):
    opt = (
        ('c', 'Coordinador'),
        ('t', 'Tecnico'),
        ('a', 'Almacenista'),
        ('v', 'Vendedor'),
    )
    ci = models.CharField(primary_key=True, max_length=10)
    nombre1 = models.CharField(max_length=15)
    nombre2 = models.CharField(max_length=15, blank=True)
    apellido1 = models.CharField(max_length=15)
    apellido2 = models.CharField(max_length=15, blank=True)
    tlf = models.CharField(max_length=15)
    correo = models.EmailField()
    dire = models.CharField(max_length=200, blank=True)
    cargo = models.CharField(max_length=1, choices=opt)
    usuario = models.OneToOneField(User)


#  aqui hay mod, estatus varchar(1) y nombre_cc dos C
class Solicitud(models.Model):
    est = (
        ('Nueva', 'Nueva'),
        ('Procesada', 'Procesada'),
        ('Atendida', 'Atendida'),
    )
    codigo = models.AutoField(primary_key=True)
    rif_c = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    disp = models.CharField(max_length=100, blank=True)
    referido_p = models.CharField(max_length=50, blank=True)
    desc = models.CharField(max_length=300)
    ubicacion = models.CharField(max_length=150)
    estatus = models.CharField(max_length=10, choices=est, default='Nueva')
    nombre_cc = models.CharField(max_length=75)
    tlf_cc = models.CharField(max_length=15)
    correo_cc = models.EmailField()
    cargo_cc = models.CharField(max_length=50)
    f_sol = models.DateField(auto_now_add=True)  # quitar null
    f_vis = models.DateField(null=True)


class Proyecto(models.Model):
    est = (
        ('Preventa', 'Preventa'),
        ('Aprobado', 'Aprobado'),
        ('Ejecucion', 'Ejecucion'),
        ('Culminado', 'Culminado'),
        ('Rechazado', 'Rechazado'),
    )
    codigo = models.CharField(primary_key=True, max_length=20)
    codigo_s = models.ForeignKey(Solicitud, on_delete=models.PROTECT)
    codigo_ri = models.ForeignKey('Reporte_inicial', on_delete=models.PROTECT,
                                  blank=True, null=True)
    ci_coord = models.ForeignKey(Trabajador, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=100)
    desc = models.CharField(max_length=500)
    ubicacion = models.CharField(max_length=150)
    estatus = models.CharField(max_length=10, choices=est, default='Preventa')
    f_ini = models.DateField(blank=True, null=True)
    f_fin = models.DateField(blank=True, null=True)
    f_est = models.DateField(blank=True, null=True)


#  se cambio estatus por completado y persona,nombre_t a 60, y fac y
#  complejidad a 2
class Reporte_inicial(models.Model):
    opt = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    )
    codigo = models.AutoField(primary_key=True)
    persona_a = models.CharField(max_length=60, blank=True)
    cargo_a = models.CharField(max_length=60, blank=True)
    desc = models.CharField(max_length=500, blank=True)
    observ = models.CharField(max_length=500, blank=True)
    factibilidad = models.CharField(max_length=2, choices=opt, blank=True)
    riesgos = models.CharField(max_length=300, blank=True)
    complejidad = models.CharField(max_length=2, choices=opt, blank=True)
    completado = models.BooleanField(default=False)
    nombre_t = models.CharField(max_length=60, blank=True)
    f_vis = models.DateField(blank=True, null=True)


class Causa_rechazo(models.Model):
    codigo = models.AutoField(primary_key=True)
    codigo_pro = models.OneToOneField(Proyecto, on_delete=models.PROTECT)
    desc = models.CharField(max_length=200)


# aqui cambio codigo p a codigo pro y estatus
class Encuesta(models.Model):
    codigo = models.AutoField(primary_key=True)
    codigo_pro = models.OneToOneField(Proyecto, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=150)
    completado = models.BooleanField(default=False)


#  aqui se cambio max lenth de pregunta a 50 y foreign key que no aparece
class Pregunta(models.Model):
    opt = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    codigo = models.AutoField(primary_key=True)
    codigo_en = models.ForeignKey(Encuesta, on_delete=models.PROTECT)
    pregunta = models.CharField(max_length=150)
    respuesta = models.CharField(max_length=1, choices=opt)


class Proyecto_tecnico(models.Model):
    codigo = models.AutoField(primary_key=True)
    codigo_pro = models.ForeignKey(Proyecto, on_delete=models.PROTECT)
    ci_tecnico = models.ForeignKey(Trabajador, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('codigo_pro', 'ci_tecnico',)


#  aqui se cambio se puso codigo y letra, estaus igual max len 1
class Etapa(models.Model):
    est = (
        ('Pendiente', 'Pendiente'),
        ('Ejecucion', 'Ejecucion'),
        #('Problemas', 'Problemas'),
        ('Culminado', 'Culminado'),
    )
    codigo = models.AutoField(primary_key=True)
    letra = models.CharField(max_length=1)
    codigo_pro = models.ForeignKey(Proyecto, on_delete=models.PROTECT)
    codigo_rd = models.ForeignKey('Reporte_detalle', on_delete=models.PROTECT,
                                  blank=True, null=True)
    nombre = models.CharField(max_length=100)
    f_ini = models.DateField(blank=True, null=True)
    f_fin = models.DateField(blank=True, null=True)
    f_est = models.DateField(blank=True, null=True)
    estatus = models.CharField(max_length=10, choices=est, default="Pendiente")
    facturada = models.BooleanField(default=False)

    class Meta:
        unique_together = ('codigo_pro', 'letra',)


#  cdigo eta y completada boolean Y NRO char max lent 5
class Actividad(models.Model):
    codigo = models.AutoField(primary_key=True)
    nro = models.CharField(max_length=5)
    codigo_eta = models.ForeignKey(Etapa, on_delete=models.PROTECT)
    desc = models.CharField(max_length=200)
    completada = models.BooleanField(default=False)

    class Meta:
        unique_together = ('codigo_eta', 'nro',)


#  persona max len 60 y completado bolean
class Reporte_detalle(models.Model):
    codigo = models.AutoField(primary_key=True)
    persona_a = models.CharField(max_length=60)
    cargo_a = models.CharField(max_length=60)
    nombre_t = models.CharField(max_length=60)
    vicios_ocu = models.CharField(max_length=500, blank=True)
    observ = models.CharField(max_length=500)
    completado = models.BooleanField(default=False)


class Reporte(models.Model):
    opt = (
        ('Avance', 'Avance'),
        ('Problema', 'Problema'),
        ('Otro', 'Otro'),
    )
    codigo = models.AutoField(primary_key=True)
    codigo_eta = models.ForeignKey(Etapa, on_delete=models.PROTECT)
    fecha = models.DateField(auto_now_add=True)
    nombre_t = models.CharField(max_length=60)
    tipo = models.CharField(max_length=10, choices=opt)
    observ = models.CharField(max_length=300)
    leido = models.BooleanField(default=False)


class Reporte_servicio(models.Model):
    codigo = models.AutoField(primary_key=True)
    codigo_ser = models.ForeignKey('Servicio', on_delete=models.PROTECT)
    codigo_rep = models.ForeignKey(Reporte, on_delete=models.PROTECT)
    cantidad = models.IntegerField()

    class Meta:
        unique_together = ('codigo_ser', 'codigo_rep',)

"""class Etapa_servicio(models.Model):
    codigo = models.AutoField(primary_key=True)
    codigo_ser = models.ForeignKey('Servicio', on_delete=models.PROTECT)
    codigo_eta = models.ForeignKey(Etapa, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('codigo_ser', 'codigo_eta',)"""


#  aqui se cambio ci vendedor por null blank true
class Presupuesto(models.Model):
    est = (
        ('Preventa', 'Preventa'),
        ('Aprobado', 'Aprobado'),
        ('Rechazado', 'Rechazado'),
    )
    codigo = models.CharField(primary_key=True, max_length=20)
    codigo_pro = models.ForeignKey(Proyecto, on_delete=models.PROTECT)
    ci_vendedor = models.ForeignKey(Trabajador, on_delete=models.PROTECT,
                                    blank=True, null=True)
    fecha = models.DateField()
    validez_o = models.IntegerField()
    descuento = models.IntegerField()
    observ = models.CharField(max_length=300, blank=True)
    desc = models.CharField(max_length=200)
    cond_g = models.CharField(max_length=500, blank=True)
    cond_p = models.CharField(max_length=500, blank=True)
    atencion_n = models.CharField(max_length=75)
    atencion_e = models.EmailField()
    estatus = models.CharField(max_length=10, choices=est, default='Preventa')


class Servicio_presupuesto(models.Model):
    codigo_pre = models.ForeignKey(Presupuesto, on_delete=models.PROTECT)
    codigo_ser = models.ForeignKey('Servicio', on_delete=models.PROTECT)
    precio_venta = models.DecimalField(max_digits=30, decimal_places=2)
    cantidad = models.IntegerField()

    class Meta:
        unique_together = ('codigo_pre', 'codigo_ser',)


class Material_presupuesto(models.Model):
    codigo_pre = models.ForeignKey(Presupuesto, on_delete=models.PROTECT)
    codigo_mat = models.ForeignKey('Material', on_delete=models.PROTECT)
    precio_venta = models.DecimalField(max_digits=30, decimal_places=4)
    cantidad = models.IntegerField()

    class Meta:
        unique_together = ('codigo_pre', 'codigo_mat',)


class Servicio(models.Model):
    codigo = models.CharField(primary_key=True, max_length=6)
    desc = models.CharField(max_length=200)
    precio_act = models.DecimalField(max_digits=30, decimal_places=2)
    f_act = models.DateField(auto_now=True)


#  serial max len 50 y varchar en las medidas
class Material(models.Model):
    codigo = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=100)
    desc = models.CharField(max_length=300, blank=True)
    presen = models.CharField(max_length=50, blank=True)
    f_act = models.DateField(auto_now=True)
    precio_act = models.DecimalField(max_digits=30, decimal_places=2)
    cantidad = models.IntegerField(blank=True, default=0)
    serial = models.CharField(max_length=50, unique=True, blank=True, null=True)
    largo = models.CharField(max_length=20, blank=True)
    ancho = models.CharField(max_length=20, blank=True)
    alto = models.CharField(max_length=20, blank=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=20, blank=True)


class Proveedor(models.Model):
    rif = models.CharField(primary_key=True, max_length=15)
    nombre = models.CharField(max_length=75)
    tlf1 = models.CharField(max_length=15)
    tlf2 = models.CharField(max_length=15, blank=True)
    dire = models.CharField(max_length=200)


class Material_proveedor(models.Model):
    codigo = models.AutoField(primary_key=True)
    codigo_prove = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    codigo_mat = models.ForeignKey(Material, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('codigo_prove', 'codigo_mat',)


#  se cambio max lent de email y buenoo el codigo del proyecto y eso nro ref ma
#  x 100
class Factura(models.Model):
    opt = (
        ('Credito', 'Credito'),
        ('Debito', 'Debito'),
        ('Efectivo', 'Efectivo'),
    )
    nro_factura = models.AutoField(primary_key=True)
    codigo_pre = models.ForeignKey(Presupuesto, on_delete=models.PROTECT)
    codigo_eta = models.OneToOneField(Etapa, on_delete=models.PROTECT)
    nro_control = models.IntegerField(unique=True)
    f_emi = models.DateField()
    f_ven = models.DateField()
    persona_cc = models.CharField(max_length=100)
    email_cc = models.CharField(max_length=100)
    cargo_cc = models.CharField(max_length=100, blank=True)
    departamento_cc = models.CharField(max_length=100, blank=True)
    cond_pago = models.CharField(max_length=10, choices=opt)
    pagada = models.BooleanField(default=False)
    banco_dest = models.CharField(max_length=100, blank=True)
    nro_ref = models.CharField(max_length=100, blank=True)
    monto_total = models.DecimalField(max_digits=50, decimal_places=4)


#  aqui el ci almacenista puede ser null por la slicitud de material, persona
#  max len 60
class Movimiento(models.Model):
    opt = (
        ('Ingreso', 'Ingreso'),
        ('Retorno', 'Retorno'),
        ('Egreso', 'Egreso'),
    )
    codigo = models.AutoField(primary_key=True)
    ci_almace = models.ForeignKey(Trabajador, on_delete=models.PROTECT,
                                  blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    tipo = models.CharField(max_length=10, choices=opt)
    completado = models.BooleanField(default=False)
    autorizado = models.BooleanField(default=False)
    f_sol = models.DateField(auto_now_add=True)
    codigo_ne = models.CharField(max_length=50, blank=True, null=True)
    codigo_oc = models.CharField(max_length=50, blank=True, null=True)
    persona_t = models.CharField(max_length=60, blank=True, null=True)
    persona_e = models.CharField(max_length=60, blank=True, null=True)
    rif_prove = models.ForeignKey(Proveedor,on_delete=models.PROTECT,
                                  blank=True, null=True)


class Material_movimiento(models.Model):
    codigo = models.AutoField(primary_key=True)
    codigo_mov = models.ForeignKey(Movimiento, on_delete=models.PROTECT)
    codigo_mat = models.ForeignKey(Material, on_delete=models.PROTECT)
    cantidad = models.IntegerField()

    class Meta:
        unique_together = ('codigo_mov', 'codigo_mat',)


class Etapa_tecnico_movimiento(models.Model):
    codigo = models.AutoField(primary_key=True)
    codigo_eta =  models.ForeignKey(Etapa, on_delete=models.PROTECT)
    ci_tecnico = models.ForeignKey(Trabajador, on_delete=models.PROTECT,
                                  blank=True)
    codigo_mov  = models.ForeignKey(Movimiento, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('codigo_mov', 'ci_tecnico', 'codigo_eta')


# aqui se cambio equ
class Equipo_movimiento(models.Model):
    codigo = models.AutoField(primary_key=True)
    codigo_mov = models.ForeignKey(Movimiento, on_delete=models.PROTECT)
    codigo_equ = models.ForeignKey('Equipo', on_delete=models.PROTECT)
    cantidad = models.IntegerField()

    class Meta:
        unique_together = ('codigo_mov', 'codigo_equ',)


class Equipo(models.Model):
    codigo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    desc = models.CharField(max_length=200, blank=True)
    costo_uso = models.DecimalField(max_digits=30, decimal_places=2)
    cantidad = models.IntegerField()
    serial = models.CharField(max_length=50, unique=True, blank=True, null=True)
    f_act = models.DateField(auto_now=True)
