from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.db import transaction

from app.permissions import esAlmacenista
from app.serializers.serializersA import MaterialSerializer, EquipoSerializer, ProveedorSerializer, MaterialProveedorSerializer
from app.models import Proyecto, Etapa, Proyecto_tecnico, Material, Equipo, Proveedor, Material_proveedor, Material_movimiento, Etapa_tecnico_movimiento, Movimiento, Trabajador


def viewsAlmacenista(arg):
    pass


"""class MaterialList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, esAlmacenista]

    queryset = Material.objects.all()
    serializer_class = MaterialSerializer"""


class MaterialList(APIView):
    permission_classes = [IsAuthenticated, esAlmacenista]

    def get(self, request, format=None):
        materiales = Material.objects.all()
        serializer = MaterialSerializer(materiales, many=True)
        for material in serializer.data:
            proveedores = Material_proveedor.objects.filter(codigo_mat=material['codigo'])
            serial = MaterialProveedorSerializer(proveedores, many=True)
            material['proveedores'] = []
            for proveedor in serial.data:
                material['proveedores'].append(proveedor['codigo_prove'])
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        if (request.data['material'] is None)or (request.data['proveedores'] is None):
            return Response("No se recibio informacion del material o los proveedores", status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic():
                material = MaterialSerializer(data=request.data['material'])
                if (material.is_valid()):
                    material.save()
                    for proveedor in request.data['proveedores']:
                        mp = {}
                        mp['codigo_prove'] = proveedor['rif']
                        mp['codigo_mat'] = material.validated_data['codigo']
                        mps = MaterialProveedorSerializer(data=mp)
                        if(mps.is_valid(raise_exception=True)):
                            mps.save()
                else:
                    return Response(material.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response(material.validated_data, status.HTTP_201_CREATED)
        except:
            return Response(mps.errors, status=status.HTTP_400_BAD_REQUEST)


class MaterialDetail(APIView):
    permission_classes = [IsAuthenticated, esAlmacenista]

    def patch(self, request, pk, format=None):
        if (request.data['material'] is None)or (request.data['proveedores'] is None):
            return Response("No se recibio informacion del material o los proveedores", status=status.HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            material = Material.objects.get(codigo=pk)
            serializer = MaterialSerializer(material, data=request.data['material'])
            if (serializer.is_valid(raise_exception=True)):
                serializer.save()
                Material_proveedor.objects.filter(codigo_mat=serializer.validated_data['codigo']).delete()
                for proveedor in request.data['proveedores']:
                    mp = {}
                    mp['codigo_prove'] = proveedor['rif']
                    mp['codigo_mat'] = serializer.validated_data['codigo']
                    mps = MaterialProveedorSerializer(data=mp)
                    if(mps.is_valid(raise_exception=True)):
                        mps.save()
                    else:
                        return Response(mps.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"msg": "Material Actualizado Satisfactoria mente"}, status=status.HTTP_200_OK)


class Disponibilidad(APIView):
    permissions= [IsAuthenticated]#aqui falta poner esALmacenistaoEsCoordindor o dejarlo asi

    def get(self, request, sol, format=None):
        try:
            mm = Material_movimiento.objects.filter(codigo_mov=sol)
            aux = {}
            tipo=""
            msg=""
            disponible = True
            aux['materiales'] = []
            for material_solicitud in mm:
                mi = Material.objects.get(codigo=material_solicitud.codigo_mat.codigo)
                if (material_solicitud.cantidad > mi.cantidad):
                    aux_2 = {}
                    aux_2['codigo_mat'] = material_solicitud.codigo_mat.codigo
                    aux_2['nombre_mat'] = material_solicitud.codigo_mat.nombre
                    aux_2['desc_mat'] = material_solicitud.codigo_mat.desc
                    aux_2['cantidad_solicitada'] = material_solicitud.cantidad
                    aux_2['cantidad_inventario'] = mi.cantidad
                    disponible = False
                    aux['materiales'].append(aux_2)
                    tipo="Sin Disponibilidad"
                    msg="Sin existencia en inventario de algunos materiales de la solicitud."
                else:
                    movimientos_materiales = Material_movimiento.objects.filter(codigo_mat=mi.codigo)
                    cont_cantidades = 0
                    for movimiento_material in movimientos_materiales:
                        if (movimiento_material.codigo_mov.autorizado==True and movimiento_material.codigo_mov.completado==False):
                            cont_cantidades = cont_cantidades + movimiento_material.cantidad
                    if ((cont_cantidades + material_solicitud.cantidad ) > mi.cantidad):
                        tipo = "Disponibilidad Limitada"
                        msg = "Existen materiales en el inventario pero ya estan aprobados para retiro en otra solicitud."
                        disponible = False
                    else:
                        tipo= "Disponibilidad"
                        msg= "Existencia de todos los materiales de la solicitud en el inventario."
            
            aux['disponible'] = disponible
            aux['tipo'] = tipo
            aux['msg'] = msg
            aux['codigo_sol'] =sol
            return Response(aux, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class MovimientoEgreso(APIView):
    permissions= [IsAuthenticated, esAlmacenista]

    def get(self, request, codigo_sol, format=None):
        try:
            #movimiento = Movimiento.objects.get(codigo=codigo_sol)
            aux = {}
            etm = Etapa_tecnico_movimiento.objects.get(codigo_mov=codigo_sol)
            mm = Material_movimiento.objects.filter(codigo_mov=codigo_sol)
            aux['codigo_sol'] = codigo_sol
            if (etm.codigo_mov.autorizado==True):
                aux['autorizado'] = "Autorizado"
            else:
                aux['autorizado'] = "No Autorizado"

            if (etm.codigo_mov.completado==True):
                aux['completado'] = "Completado"
            else:
                aux['completado'] = "No Completado"
            aux['ci_tecnico'] = etm.ci_tecnico.ci
            aux['nombre_t'] = etm.ci_tecnico.nombre1 +" " + etm.ci_tecnico.nombre2 +" " + etm.ci_tecnico.apellido1 +" " +etm.ci_tecnico.apellido2
            aux['materiales'] = []
            for material in mm:
                aux_2={}
                aux_2['codigo'] = material.codigo_mat.codigo
                aux_2['nombre'] = material.codigo_mat.nombre
                aux_2['desc']  = material.codigo_mat.desc
                aux_2['serial']  = material.codigo_mat.serial
                aux_2['cantidad'] = material.cantidad
                aux['materiales'].append(aux_2)

            return Response(aux,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, codigo_sol, format=None):
        try:
            with transaction.atomic():
                movimiento = Movimiento.objects.get(codigo=codigo_sol)
                if (movimiento.autorizado==True and movimiento.completado==False):
                    mm = Material_movimiento.objects.filter(codigo_mov=codigo_sol)
                    for material in mm:
                        mat = Material.objects.get(codigo=material.codigo_mat.codigo)
                        mat.cantidad = (mat.cantidad - material.cantidad)
                        mat.save()
                        print(mat.cantidad)
                    movimiento.completado = True
                    movimiento.fecha = request.data['fecha']
                    movimiento.ci_almacenista = Trabajador.objects.get(ci=request.data['ci_almacenista'])
                    movimiento.tipo = request.data['tipo']
                    movimiento.save()
                    data = {}
                    data['data'] = None
                    data['msg'] = "Egreso procesado exitosamente."
                    return Response(data,status=status.HTTP_200_OK)
                else:
                    return Response("El movimiento no ha sido autorizado o ya fue procesado.",status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class MovimientoIngreso(APIView):
    permissions= [IsAuthenticated, esAlmacenista]

    def get(self, request, rif_prove, format=None):
        try:
            print(rif_prove)
            return Response("ok",status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class MovimientoRetorno(APIView):
    permissions= [IsAuthenticated, esAlmacenista]

    def get(self, request, codigo_pro, format=None):
        try:
            data = {}
            proyecto = Proyecto.objects.get(codigo=codigo_pro) 
            data['codigo_pro'] = proyecto.codigo
            data['nombre_pro'] = proyecto.nombre
            data['etapas'] = []
            data['tecnicos'] = []
            data['materiales'] = []
            etapas = Etapa.objects.filter(codigo_pro=codigo_pro)
            for etapa in etapas:
                aux = {}
                aux['codigo_eta']= etapa.codigo
                aux['nombre_eta']= etapa.nombre
                aux['letra_eta']= etapa.letra
                data['etapas'].append(aux)
                etms = Etapa_tecnico_movimiento.objects.filter(codigo_eta=etapa.codigo)
                for etm in etms:
                    if (etm.codigo_mov.completado==True and etm.codigo_mov.tipo == "Egreso"):
                        mm = Material_movimiento.objects.filter(codigo_mov=etm.codigo_mov.codigo)
                        for material in mm:
                            aux = {}
                            aux['codigo'] = material.codigo_mat.codigo
                            aux['nombre'] = material.codigo_mat.nombre
                            aux['desc'] = material.codigo_mat.desc
                            aux['serial'] = material.codigo_mat.serial
                            aux['cantidad'] = material.cantidad
                            data['materiales'].append(aux)
                        #aux['codigo_eta'] = etapa.codigo
                        #aux['nombre_eta'] = etapa.nombre
            tecnicos = Proyecto_tecnico.objects.filter(codigo_pro=codigo_pro)
            for tecnico in tecnicos:
                aux={}
                aux['ci_tecnico']=tecnico.ci_tecnico.ci
                aux['nombre_t'] = tecnico.ci_tecnico.nombre1 + " "+tecnico.ci_tecnico.nombre2 + " "+tecnico.ci_tecnico.apellido1 + " "+tecnico.ci_tecnico.apellido2
                data['tecnicos'].append(aux)
            return Response(data,status=status.HTTP_200_OK)
        except Proyecto.DoesNotExist:
            return Response("No existe un proyecto con ese codigo: "+codigo_pro, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


    def post(self, request, codigo_pro, format=None):
        try:
            with transaction.atomic():
                if not request.data['materiales']:
                    return Response("No se ha incluido ningun material en el retorno, favor seleccionar alguno(s).", status=status.HTTP_400_BAD_REQUEST)
                print(request.data)
                #movimiento = bar = BarModel.objects.create()
                #movimiento.
                return Response("ok",status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

class EquipoList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, esAlmacenista]

    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer


class EquipoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, esAlmacenista]

    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer


class ProveedorList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, esAlmacenista]

    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer


class ProveedorDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, esAlmacenista]

    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer