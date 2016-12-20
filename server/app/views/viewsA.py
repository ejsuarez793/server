from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
import json
from django.db import transaction, IntegrityError

from app.permissions import esAlmacenista
from app.serializers.serializersA import MaterialSerializer, EquipoSerializer, ProveedorSerializer, MaterialProveedorSerializer
from app.models import Material, Equipo, Proveedor, Material_proveedor


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