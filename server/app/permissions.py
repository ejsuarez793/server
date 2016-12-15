from rest_framework import permissions
from django.contrib.auth.models import User
from app.models import Trabajador
from rest_framework.response import Response


SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']

class esAlmacenista(permissions.BasePermission):
    message = 'El usuario no es un Almacenista, o esta ejecutando un metodo no permitido.'

    def has_permission(self, request, view):
        try:
            usuario = User.objects.get(username=request.user)
            trabajador = Trabajador.objects.get(usuario_id=usuario.id)
            if (trabajador.cargo == "a" or request.method in SAFE_METHODS):
                return True
            else:
                return False
        except:
            return False


class esCoordinador(permissions.BasePermission):
    message = 'El usuario no es un Coordinador.'

    def has_permission(self, request, view):
        try:
            usuario = User.objects.get(username=request.user)
            trabajador = Trabajador.objects.get(usuario_id=usuario.id)
            if (trabajador.cargo == "c" or request.method in SAFE_METHODS):
                return True
            else:
                return False
        except:
            return False


class esTecnicoOsoloLectura(permissions.BasePermission):
    message = 'El usuario no es un Tecnico,o esta ejecutando un metodo no permitido.'

    def has_permission(self, request, view):
        try:
            usuario = User.objects.get(username=request.user)
            trabajador = Trabajador.objects.get(usuario_id=usuario.id)
            if (trabajador.cargo == "t" or request.method in SAFE_METHODS):
                return True
            else:
                return False
        except:
            return False


class esVendedor(permissions.BasePermission):
    message = 'El usuario no es un Vendedor.'

    def has_permission(self, request, view):
        try:
            usuario = User.objects.get(username=request.user)
            trabajador = Trabajador.objects.get(usuario_id=usuario.id)
            if (trabajador.cargo == "v"):
                return True
            else:
                return False
        except:
            return False


"""class esCoordinadorOesTecnico(permissions.BasePermission):
    message = 'El usuario no es Coordinador o Tecnico.'

    def has_permission(self, request, view):
        try:
            usuario = User.objects.get(username=request.user)
            trabajador = Trabajador.objects.get(usuario_id=usuario.id)
            if (trabajador.cargo == "c" or trabajador.cargo == "t"):
                return True
            else:
                return False
        except:
            return False"""
