from django.contrib.auth.models import User
from app.models import Trabajador, Presupuesto, Movimiento, Proyecto, Proyecto_tecnico, Etapa_tecnico_movimiento
from app.serializers.serializersAll import UserSerializer, TrabajadorSerializer
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction


def viewsAdministrador(arg):
    pass


class GestionUsuario(APIView):
    permissions_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, ci, format=None):
        try:
            trabajador = Trabajador.objects.get(ci=ci)
            flag = False
            if(trabajador.cargo=="a"):
                print("almacenista")
                movimientos = Movimiento.objects.filter(ci_almace=ci)
                if not movimientos:
                    flag = True
            elif(trabajador.cargo=="c"):
                proyectos = Proyecto.objects.filter(ci_coord=ci)
                if not proyectos:
                    flag = True
                print("coordinador")
            elif(trabajador.cargo=="v"):
                presupuestos = Presupuesto.objects.filter(ci_vendedor=ci)
                if not presupuestos:
                    flag = True
                print("vendedor")
            elif(trabajador.cargo=="t"):
                print("tecnico")
                pt = Proyecto_tecnico.objects.filter(ci_tecnico=ci)
                etm = Etapa_tecnico_movimiento.objects.filter(ci_tecnico=ci)
                if(not pt and not etm):
                    flag = True
            if(flag==True):
                trabajador.cargo = request.data
                trabajador.save()

                data = {}
                data['data'] = None
                data['msg'] = "Rol de usuario cambiado exitosamente."
            else:
                return Response("El rol de usuario no se puede cambiar, ya es un usuario activo.", status=status.HTTP_400_BAD_REQUEST)
            return Response(data, status=status.HTTP_200_OK)
        except Trabajador.DoesNotExist:
            return Response("No hay un usuario registrado con esa cedula.", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class ClaveUsuario(APIView):
    permissions_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, ci, format=None):
        try:
            trabajador = Trabajador.objects.get(ci=ci)
            trabajador.usuario.set_password(request.data['password1'])
            trabajador.usuario.save()
            data = {}
            data['data'] = None
            data['msg'] = "Clave de usuario cambiado exitosamente."
            return Response(data, status=status.HTTP_200_OK)
        except Trabajador.DoesNotExist:
            return Response("No hay un usuario registrado con esa cedula.", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)