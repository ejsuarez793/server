from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.db import transaction

from app.permissions import esAlmacenista
from app.serializers.serializersA import MaterialSerializer, ProveedorSerializer, MaterialProveedorSerializer
from app.models import Proyecto, Etapa, Proyecto_tecnico, Material, Proveedor, Material_proveedor, Material_movimiento, Etapa_tecnico_movimiento, Movimiento, Trabajador


def viewsAlmacenista(arg):
    pass


"""class MaterialList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, esAlmacenista]

    queryset = Material.objects.all()
    serializer_class = MaterialSerializer"""


class MaterialList(APIView):
    permission_classes = [IsAuthenticated, esAlmacenista]

    def get(self, request, format=None):
        materiales = Material.objects.all().order_by('codigo')
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
                data = {}
                data['data'] = material.validated_data
                data['msg'] = "Material creado exitosamente."
                return Response(data, status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


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
            return Response({"msg": "Material Actualizado exitosamente."}, status=status.HTTP_200_OK)


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
    permissions = [IsAuthenticated, esAlmacenista]

    def get(self, request, codigo_sol, format=None):
        try:
            Movimiento.objects.get(codigo=codigo_sol)
            aux = {}
            etm = Etapa_tecnico_movimiento.objects.get(codigo_mov=codigo_sol)
            mm = Material_movimiento.objects.filter(codigo_mov=codigo_sol)
            aux['codigo_sol'] = codigo_sol
            if (etm.codigo_mov.autorizado is True):
                aux['autorizado'] = "Autorizado"
            else:
                aux['autorizado'] = "No Autorizado"

            if (etm.codigo_mov.completado is True):
                aux['completado'] = "Completado"
            else:
                aux['completado'] = "No Completado"
            aux['ci_tecnico'] = etm.ci_tecnico.ci
            aux['nombre_t'] = etm.ci_tecnico.nombre1 + " " + etm.ci_tecnico.nombre2 + " " + etm.ci_tecnico.apellido1 + " " + etm.ci_tecnico.apellido2
            aux['materiales'] = []
            for material in mm:
                aux_2 = {}
                aux_2['codigo'] = material.codigo_mat.codigo
                aux_2['nombre'] = material.codigo_mat.nombre
                aux_2['desc'] = material.codigo_mat.desc
                aux_2['serial'] = material.codigo_mat.serial
                aux_2['cantidad'] = material.cantidad
                aux['materiales'].append(aux_2)

            return Response(aux, status=status.HTTP_200_OK)
        except Movimiento.DoesNotExist:
            return Response("No existe una solicitud de egreso con ese codigo: " + codigo_sol, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, codigo_sol, format=None):
        try:
            with transaction.atomic():
                movimiento = Movimiento.objects.get(codigo=codigo_sol)
                if (movimiento.autorizado is True and movimiento.completado is False):
                    mm = Material_movimiento.objects.filter(codigo_mov=codigo_sol)
                    for material in mm:
                        mat = Material.objects.get(codigo=material.codigo_mat.codigo)
                        mat.cantidad = (mat.cantidad - material.cantidad)
                        mat.save()
                        print(mat.cantidad)
                    movimiento.completado = True
                    movimiento.fecha = request.data['fecha']
                    movimiento.ci_almace = Trabajador.objects.get(ci=request.data['ci_almacenista'])
                    movimiento.tipo = request.data['tipo']
                    movimiento.save()
                    data = {}
                    data['data'] = None
                    data['msg'] = "Egreso procesado exitosamente."
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    return Response("El movimiento no ha sido autorizado o ya fue completado.", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class MovimientoIngreso(APIView):
    permissions = [IsAuthenticated, esAlmacenista]

    def get(self, request, rif_prove, format=None):
        try:
            proveedor = Proveedor.objects.get(rif=rif_prove)
            data = {}
            data['rif_prove'] = proveedor.rif
            data['nombre_prove'] = proveedor.nombre
            data['materiales'] = []
            materiales = Material.objects.all()
            for material in materiales:
                aux = {}
                aux['codigo'] = material.codigo
                aux['nombre'] = material.nombre
                aux['desc'] = material.desc
                aux['serial'] = material.serial
                aux['cantidad'] = material.cantidad
                if (aux['serial'] is not None and aux['cantidad'] == 0):  # si el material tiene serial, y solo si la cantidad
                    data['materiales'].append(aux)                   # es 0 se puede agregar
                elif(aux['serial'] is None):  # si no tiene serial se puede agregar normalmente
                    data['materiales'].append(aux)

            return Response(data, status=status.HTTP_200_OK)
        except Proveedor.DoesNotExist:
            return Response("No existe un proveedor con ese rif: " + rif_prove, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


    def post(self, request, rif_prove, format=None):
        try:
            with transaction.atomic():
                if not request.data['materiales']:
                    return Response("No se ha incluido ningun material en el ingreso, favor seleccionar alguno(s).", status=status.HTTP_400_BAD_REQUEST)
                # creamos el movimiento
                movimiento = Movimiento.objects.create()
                movimiento.fecha = request.data['fecha']
                movimiento.completado = request.data['completado']
                movimiento.codigo_ne = request.data['codigo_ne']
                movimiento.codigo_oc = request.data['codigo_oc']
                movimiento.ci_almace = Trabajador.objects.get(ci=request.data['ci_almace'])
                movimiento.persona_t = request.data['persona_t']
                movimiento.persona_e = request.data['persona_e']
                movimiento.tipo = request.data['tipo']
                movimiento.rif_prove = Proveedor.objects.get(rif=rif_prove)
                movimiento.save()

                # asociamos los materiales al movimiento y sumamos las cantidades ingresadas al inventario
                for material in request.data['materiales']:
                    mat = Material.objects.get(codigo=material['codigo'])
                    Material_movimiento.objects.create(cantidad=material['cantidad'], codigo_mov=movimiento, codigo_mat=mat)

                    mat.cantidad += material['cantidad']
                    mat.save()

                # ahora asociamos los materiales al codigo del proveedor, si es que no lo tienen ya asociado
                proveedor = Proveedor.objects.get(rif=rif_prove)
                mps = Material_proveedor.objects.filter(codigo_prove=rif_prove)
                flag = False
                for material in request.data['materiales']:
                    flag = False
                    for material_proveedor in mps:
                        if(material_proveedor.codigo_mat.codigo == material['codigo']):
                            flag = True
                    if (flag is False):
                        material = Material.objects.get(codigo=material['codigo'])
                        Material_proveedor.objects.create(codigo_mat=material, codigo_prove=proveedor)

                data = {}
                data['data'] = None
                data['msg'] = "Ingreso procesado exitosamente."
                return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class MovimientoRetorno(APIView):
    permissions = [IsAuthenticated, esAlmacenista]

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
                aux['codigo_eta'] = etapa.codigo
                aux['nombre_eta'] = etapa.nombre
                aux['letra_eta'] = etapa.letra
                data['etapas'].append(aux)
                etms = Etapa_tecnico_movimiento.objects.filter(codigo_eta=etapa.codigo)
                for etm in etms:
                    if (etm.codigo_mov.completado is True and etm.codigo_mov.tipo == "Egreso"):
                        mm = Material_movimiento.objects.filter(codigo_mov=etm.codigo_mov.codigo)
                        for material in mm:
                            aux = {}
                            aux['codigo'] = material.codigo_mat.codigo
                            aux['nombre'] = material.codigo_mat.nombre
                            aux['desc'] = material.codigo_mat.desc
                            aux['serial'] = material.codigo_mat.serial
                            aux['cantidad'] = material.cantidad
                            data['materiales'].append(aux)

                for etm in etms:
                    if (etm.codigo_mov.completado is True and etm.codigo_mov.tipo == "Retorno"):
                        mm = Material_movimiento.objects.filter(codigo_mov=etm.codigo_mov.codigo)
                        for material in mm:
                            for mat_egresado in data['materiales']:
                                if (mat_egresado['codigo'] == material.codigo_mat.codigo):
                                    mat_egresado['cantidad'] -= material.cantidad
                                    if (mat_egresado['cantidad'] == 0):
                                        data['materiales'].remove(mat_egresado)

            tecnicos = Proyecto_tecnico.objects.filter(codigo_pro=codigo_pro)
            for tecnico in tecnicos:
                aux = {}
                aux['ci_tecnico'] = tecnico.ci_tecnico.ci
                aux['nombre_t'] = tecnico.ci_tecnico.nombre1 + " " + tecnico.ci_tecnico.nombre2 + " " + tecnico.ci_tecnico.apellido1 + " " + tecnico.ci_tecnico.apellido2
                data['tecnicos'].append(aux)
            return Response(data, status=status.HTTP_200_OK)
        except Proyecto.DoesNotExist:
            return Response("No existe un proyecto con ese codigo: " + codigo_pro, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, codigo_pro, format=None):
        try:
            with transaction.atomic():
                if not request.data['materiales']:
                    return Response("No se ha incluido ningun material en el retorno, favor seleccionar alguno(s).", status=status.HTTP_400_BAD_REQUEST)

                movimiento = Movimiento.objects.create()
                movimiento.ci_almace = Trabajador.objects.get(ci=request.data['ci_almace'])
                movimiento.fecha = request.data['fecha']
                movimiento.tipo = request.data['tipo']
                movimiento.completado = True
                movimiento.save()

                for material in request.data['materiales']:
                    Material_movimiento.objects.create(cantidad=material['cantidad'], codigo_mov=movimiento, codigo_mat=Material.objects.get(codigo=material['codigo']))

                codigo_eta = Etapa.objects.get(codigo=request.data['codigo_eta'])
                ci_tecnico = Trabajador.objects.get(ci=request.data['ci_tecnico'])

                Etapa_tecnico_movimiento.objects.create(ci_tecnico=ci_tecnico, codigo_eta=codigo_eta, codigo_mov=movimiento)

                data = {}
                data['data'] = None
                data['msg'] = "Retorno procesado exitosamente."
                return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class ConsultaRango(APIView):
    def get(self, request, tipo, desde, hasta, format=None):
        try:
            #print(desde)
            #print(hasta)
            #print(tipo)
            if(tipo == "rango"):
                movimientos = Movimiento.objects.filter(fecha__range=(desde, hasta)).order_by('codigo')
            elif(tipo == "mes"):
                movimientos = Movimiento.objects.filter(fecha__month=(desde)).order_by('codigo')
            movs = {}
            movs['movimientos'] = []
            for movimiento in movimientos:
                if (movimiento.completado is True):
                    aux = {}
                    aux['codigo'] = movimiento.codigo
                    aux['fecha'] = movimiento.fecha
                    aux['tipo'] = movimiento.tipo
                    aux['ci_almace'] = movimiento.ci_almace.ci
                    aux['nombre_almace'] = movimiento.ci_almace.nombre1 + " " + movimiento.ci_almace.apellido1 + " " + movimiento.ci_almace.apellido2
                    aux['codigo_ne'] = movimiento.codigo_ne
                    aux['codigo_oc'] = movimiento.codigo_oc
                    aux['persona_t'] = movimiento.persona_t
                    aux['persona_e'] = movimiento.persona_e
                    aux['materiales'] = []
                    mm = Material_movimiento.objects.filter(codigo_mov=movimiento)
                    for material in mm:
                        aux_2 = {}
                        aux_2['codigo'] = material.codigo_mat.codigo
                        aux_2['nombre'] = material.codigo_mat.nombre
                        aux_2['desc'] = material.codigo_mat.desc
                        aux_2['serial'] = material.codigo_mat.serial
                        aux_2['cantidad'] = material.cantidad
                        aux['materiales'].append(aux_2)

                    if (movimiento.tipo == "Egreso" or movimiento.tipo == "Retorno"):
                        etm = Etapa_tecnico_movimiento.objects.get(codigo_mov=movimiento)
                        aux['codigo_pro'] = etm.codigo_eta.codigo_pro.codigo
                        aux['nombre_pro'] = etm.codigo_eta.codigo_pro.nombre
                        aux['letra_eta'] = etm.codigo_eta.letra
                        aux['nombre_eta'] = etm.codigo_eta.nombre
                        aux['ci_tecnico'] = etm.ci_tecnico.ci
                        aux['nombre_tec'] = etm.ci_tecnico.nombre1 + " " + etm.ci_tecnico.apellido1 + " " + etm.ci_tecnico.apellido2
                        aux['rif_prove'] = ""
                        aux['nombre_prove'] = ""
                    else:

                        aux['codigo_pro'] = ""
                        aux['nombre_pro'] = ""
                        aux['letra_eta'] = ""
                        aux['ci_tecnico'] = ""
                        aux['nombre_tec'] = ""
                        aux['rif_prove'] = movimiento.rif_prove.rif
                        aux['nombre_prove'] = movimiento.rif_prove.nombre
                    aux['mostrar'] = True
                    movs['movimientos'].append(aux)

            data = {}
            data['data'] = movs
            if not data['data']['movimientos']:
                msg = "La consulta no dio resultados."
            else:
                msg = "Consulta existosa."
            data['msg'] = msg
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class ValidarMaterial(APIView):
    def get(self, request, format=None):
        codigo = self.request.query_params.get('codigo')
        try:
            Material.objects.get(codigo=codigo) # retrieve the user using username
        except Material.DoesNotExist: # si es usuario no existe es un username valido
            return Response("true")
        else:
            return Response("Material ya existe.") 


class ValidarProveedor(APIView):
    def get(self, request, format=None):
        rif = self.request.query_params.get('rif')
        try:
            Proveedor.objects.get(rif=rif) # retrieve the user using username
        except Proveedor.DoesNotExist: # si es usuario no existe es un username valido
            return Response("true")
        else:
            return Response("Proveedor ya existe.") 


"""class EquipoList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, esAlmacenista]

    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer


class EquipoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, esAlmacenista]

    queryset = Equipo.objects.all().order_by('rif')
    serializer_class = EquipoSerializer"""


class ProveedorList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, esAlmacenista]

    queryset = Proveedor.objects.all().order_by('rif')
    serializer_class = ProveedorSerializer


class ProveedorDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, esAlmacenista]

    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer