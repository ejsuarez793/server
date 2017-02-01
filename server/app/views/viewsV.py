from app.models import Cliente, Solicitud
from app.serializers.serializersV import ClienteSerializer, SolicitudSerializer, Causa_rechazoSerializer
from rest_framework.views import APIView

from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from decimal import Decimal

from app.permissions import esVendedor
from app.serializers.serializersV import ProyectoEstatusSerializer, PresupuestoSerializer, EncuestaSerializer, PreguntaSerializer, FacturaSerializer
from app.models import Proyecto, Presupuesto, Material_presupuesto, Servicio_presupuesto, Reporte, Reporte_servicio, Etapa_tecnico_movimiento, Material_movimiento, Etapa, Factura


def viewsVendedor(arg):
    pass


"""class ClienteList(generics.ListCreateAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer"""


"""class ClienteDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer"""



"""class SolicitudList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer"""

class ClienteList(APIView):
    permission_classes = [IsAuthenticated, esVendedor]

    def get(self, request, format=None):
        try:
            clientes = Cliente.objects.all()
            data = []
            for cliente in clientes:
                aux = {}
                aux['rif'] = cliente.rif
                aux['nombre'] = cliente.nombre
                aux['tlf1'] = cliente.tlf1
                aux['tlf2'] = cliente.tlf2
                aux['fax'] = cliente.fax
                aux['dire'] = cliente.dire
                aux['act_eco'] = cliente.act_eco
                aux['cond_contrib'] = cliente.cond_contrib
                data.append(aux)
            return Response(data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        try:
            s_cliente = ClienteSerializer(data=request.data)
            if (s_cliente.is_valid(raise_exception=True)):
                s_cliente.save()
                data = {}
                data['data'] = s_cliente.data
                data['msg'] = "Cliente creado exitosamente."
                return Response(data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class ClienteDetail(APIView):
    permission_classes = [IsAuthenticated, esVendedor]

    def get(self, request, pk, format=None):
        try:
            cliente = Cliente.objects.get(rif=pk)
            s_cliente = ClienteSerializer(data=cliente)
            if (s_cliente.is_valid(raise_exception=True)):
                return Response(s_cliente.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        try:
            cliente = Cliente.objects.get(rif=pk)
            s_cliente = ClienteSerializer(cliente, data=request.data)
            if (s_cliente.is_valid(raise_exception=True)):
                s_cliente.save()
                data = {}
                data['data'] = s_cliente.data
                data['msg'] = "Cliente editado exitosamente"
                return Response(data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)



class SolicitudList(APIView):
    permission_classes = [IsAuthenticated, esVendedor]

    def get(self, request, format=None):
        try:
            solicitudes = Solicitud.objects.all()
            data = []
            for solicitud in solicitudes:
                aux={}
                aux['codigo'] = solicitud.codigo
                aux['rif_c'] = solicitud.rif_c.rif
                aux['disp'] = solicitud.disp
                aux['referido_p'] = solicitud.referido_p
                aux['desc'] = solicitud.desc
                aux['ubicacion'] = solicitud.ubicacion
                aux['estatus'] = solicitud.estatus
                aux['nombre_cc'] = solicitud.nombre_cc
                aux['tlf_cc'] = solicitud.tlf_cc
                aux['correo_cc'] = solicitud.correo_cc
                aux['cargo_cc'] = solicitud.cargo_cc
                aux['f_sol'] = solicitud.f_sol
                aux['f_vis'] = solicitud.f_vis
                aux['nombre_cliente'] = solicitud.rif_c.nombre
                aux['tlf1'] = solicitud.rif_c.tlf1
                aux['tlf2'] = solicitud.rif_c.tlf2
                aux['fax'] = solicitud.rif_c.fax
                data.append(aux)
            return Response(data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


    def post(self, request, format=None):
        try:
            s_solicitud = SolicitudSerializer(data=request.data)
            if (s_solicitud.is_valid(raise_exception=True)):
                s_solicitud.save()
                data = {}
                data['data'] = s_solicitud.data
                data['msg'] = "Solicitud creado exitosamente."
                return Response(data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)




class ProyectoProcesarEstatus(APIView):
    permission_classes = [esVendedor]

    def patch(self, request, pk, format=None):
        try:
            with transaction.atomic():
                proyecto = Proyecto.objects.get(codigo=pk)
                if(proyecto.estatus != "Aprobado"):
                    s_proyecto = ProyectoEstatusSerializer(proyecto, data=request.data)
                    if(s_proyecto.is_valid(raise_exception=True)):
                        presupuestos = Presupuesto.objects.filter(codigo_pro=s_proyecto.validated_data['codigo'])
                        s_presupuestos = PresupuestoSerializer(presupuestos, many=True)
                        if(s_proyecto.validated_data['estatus']=="Aprobado"):
                            flag = False
                            for presupuesto in s_presupuestos.data:
                                if (presupuesto['estatus']=="Preventa"):
                                    return Response("Proyecto tiene un presupuesto que sigue en preventa",status=status.HTTP_400_BAD_REQUEST)
                            for presupuesto in s_presupuestos.data:
                                if (presupuesto['estatus']=="Rechazado"):
                                    print("p")
                                    #Material_presupuesto.objects.filter(codigo_pre=presupuesto['codigo']).delete()
                                    #Servicio_presupuesto.objects.filter(codigo_pre=presupuesto['codigo']).delete()
                                    #Presupuesto.objects.get(codigo=presupuesto['codigo']).delete()

                        elif(s_proyecto.validated_data['estatus']=="Rechazado"):
                            flag = False
                            for presupuesto in s_presupuestos.data:
                                if (presupuesto['estatus']!="Rechazado"):
                                    flag = True
                            if (flag==True):
                                return Response("Proyecto tiene un presupuesto que no ha sido rechazado",status=status.HTTP_400_BAD_REQUEST)
                        s_proyecto.save()
                        msg = "Proyecto " +s_proyecto.validated_data['estatus']+" Exitosamente!"
                        data = {}
                        data['data'] = s_proyecto.data
                        data['msg'] = msg
                return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class ProyectoCausaRechazo(APIView):
    permission_classes = [esVendedor]

    def post(self, request, pk, format=None):
        try:
            s_causa_rechazo = Causa_rechazoSerializer(data=request.data)
            if(s_causa_rechazo.is_valid(raise_exception=True)):
                s_causa_rechazo.save()
                msg = "Causa de rechazo almacenada exitosamente!"

                data = {}
                data['data'] = s_causa_rechazo.data
                data['msg'] = msg
                return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class ProyectoEncuesta(APIView):

     def post(self, request, pk, format=None):
        try:
            with transaction.atomic():
                s_encuesta = EncuestaSerializer(data=request.data['encuesta'])
                if (s_encuesta.is_valid(raise_exception=True)):
                    s_encuesta.save()
                    s_preguntas = PreguntaSerializer(data=request.data['preguntas'],many=True)
                    for pregunta in s_preguntas.initial_data:
                        pregunta['codigo_en'] = s_encuesta.data['codigo']
                    if(s_preguntas.is_valid(raise_exception=True)):
                        s_preguntas.save()
                        s_encuesta.data['preguntas'] = s_preguntas.data
                    msg = "Encuesta completada exitosamente!"
                    data = {}
                    data['data'] = s_encuesta.data
                    data['msg'] = msg
                return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class FacturaConsultar(APIView):
    permission_classes = [IsAuthenticated, esVendedor]

    def get(self, request, cod_eta, cod_pre, format=None):
        try:
            with transaction.atomic():
                elementos_presupuesto = []

                materiales_presupuesto = Material_presupuesto.objects.filter(codigo_pre=cod_pre)
                for material in materiales_presupuesto:
                    aux={}
                    aux['codigo'] = material.codigo_mat.codigo
                    aux['desc'] = material.codigo_mat.nombre
                    aux['precio_unitario'] = material.precio_venta
                    aux['cantidad'] = material.cantidad
                    elementos_presupuesto.append(aux)

                servicios_presupuesto = Servicio_presupuesto.objects.filter(codigo_pre=cod_pre)
                for servicio in servicios_presupuesto:
                    aux={}
                    aux['codigo'] = servicio.codigo_ser.codigo
                    aux['desc'] = servicio.codigo_ser.desc
                    aux['precio_unitario'] = servicio.precio_venta
                    aux['cantidad'] = servicio.cantidad
                    elementos_presupuesto.append(aux)

                #print(elementos_presupuesto)
                elementos_etapa = []
                reportes = Reporte.objects.filter(codigo_eta=cod_eta)
                for reporte in reportes:
                    servicios_reporte = Reporte_servicio.objects.filter(codigo_rep=reporte.codigo)
                    for servicio in servicios_reporte:
                        aux={}
                        aux['codigo'] = servicio.codigo_ser.codigo
                        aux['desc'] = servicio.codigo_ser.desc
                        aux['cantidad'] = servicio.cantidad
                        elementos_etapa.append(aux)
                
                #print(elementos_etapa)
                egresados = []
                retornados = []
                etms = Etapa_tecnico_movimiento.objects.filter(codigo_eta=cod_eta)
                for etm in etms:
                    if (etm.codigo_mov.completado==True):
                        mm = Material_movimiento.objects.filter(codigo_mov=etm.codigo_mov.codigo)
                        for material in mm:
                            aux = {}
                            aux['codigo'] = material.codigo_mat.codigo
                            aux['desc'] = material.codigo_mat.desc
                            aux['cantidad'] = material.cantidad
                            if (etm.codigo_mov.tipo == "Egreso"):
                                egresados.append(aux)
                            elif(etm.codigo_mov.tipo == "Retorno"):
                                retornados.append(aux)

                #print(egresados)
                #print(retornados)
                #usados = []
                for egresado in egresados:
                    for retornado in retornados:
                        if (egresado['codigo'] == retornado['codigo']):
                            egresado['cantidad'] = egresado['cantidad'] - retornado['cantidad']


                for egresado in egresados:
                    if (egresado['cantidad']!=0):
                        elementos_etapa.append(egresado)

                #print(elementos_presupuesto)
                #print(elementos_etapa)
                subtotal1 = 0
                for elemento_etapa in elementos_etapa:
                    flag = False
                    for elemento_presupuesto in elementos_presupuesto:
                        if (elemento_presupuesto['codigo'] == elemento_etapa['codigo']):
                            elemento_etapa['precio_unitario'] = elemento_presupuesto['precio_unitario']
                            elemento_etapa['precio_total'] = elemento_etapa['cantidad'] * elemento_etapa['precio_unitario']
                            subtotal1 +=elemento_etapa['precio_total']
                            flag = True
                    if (flag==False):
                        return Response('Hay un elemento que no se encuentra en el presupuesto, revisar presupuesto seleccionado.',status=status.HTTP_400_BAD_REQUEST)

                #print(elementos_etapa)
                #msg = "Etapa facturada exitosamente!"
                descuento_p = Presupuesto.objects.get(codigo=cod_pre)
                descuento = subtotal1 * (descuento_p.descuento/Decimal(100))
                subtotal_final = subtotal1 - descuento
                iva = subtotal_final *  Decimal(0.12)
                total = subtotal_final + iva
                data = {}
                data['elementos'] = elementos_etapa
                data['subtotal1'] = subtotal1
                data['descuento'] = descuento
                data['descuento_p'] = descuento_p.descuento
                data['subtotal_final'] = subtotal_final
                data['iva'] = iva
                data['total'] = total
                data['codigo_pre'] = cod_pre
                data['codigo_eta'] = cod_eta
                #data['data'] = None
                #data['msg'] = msg
                return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class FacturaEtapa(APIView):
    permission_classes = [IsAuthenticated, esVendedor]

    def post(self, request, cod_eta, format=None):
        try:
            with transaction.atomic():
                print(request.data)
                s_factura = FacturaSerializer(data=request.data)
                if(s_factura.is_valid(raise_exception=True)):
                    s_factura.save()
                    etapa = Etapa.objects.get(codigo=cod_eta)
                    etapa.facturada = True
                    etapa.save()
                else:
                    print(s_factura.errors)
                msg = "Etapa facturada exitosamente."
                data = {}
                data['data'] = None
                data['msg'] = msg
                return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, cod_eta, format=None):
        try:
            with transaction.atomic():
                factura = Factura.objects.get(codigo_eta=cod_eta)
                factura.banco_dest = request.data['banco_dest']
                factura.pagada = request.data['pagada']
                factura.nro_ref = request.data['nro_ref']
                factura.save()
                msg = "Pago de factura guardado exitosamente."
                data = {}
                data['data'] = None
                data['msg'] = msg
                return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)