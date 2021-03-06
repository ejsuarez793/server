from django.contrib.auth.models import User
from app.models import Trabajador,Cliente,Servicio
from app.serializers.serializersAll import UserSerializer, TrabajadorSerializer
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication
from django.db import transaction


def viewsTodos(arg):
    pass


class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)

    def post(self, request, format=None):
        try:
            with transaction.atomic():
                serializer = UserSerializer(data=request.data['user'])
                if serializer.is_valid(raise_exception=True):
                    user = User.objects.create_user(
                        serializer.validated_data['username'],
                        serializer.validated_data['email'],
                        serializer.validated_data['password']
                    )
                    request.data['trabajador']['usuario'] = user.pk
                    serializer1 = TrabajadorSerializer(data=request.data['trabajador'])
                    if serializer1.is_valid(raise_exception=True):
                        serializer1.save()
                        data = {}
                        data['data'] = serializer1.data
                        data['msg'] = "Usuario registrado exitosamente."
                        return Response(data, status=status.HTTP_201_CREATED)
                    else:
                        instance = User.objects.get(id= user.pk)
                        instance.delete()
                        return Response(serializer1.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)



class ValidarUsuario(APIView):
    def get(self, request, format=None):
        username = self.request.query_params.get('username')
        try:
            User.objects.get(username=username) # retrieve the user using username
        except User.DoesNotExist: # si es usuario no existe es un username valido
            return Response("true")
        else:
            return Response("Usuario ya existe.") 


class ValidarTrabajador(APIView):
    def get(self, request, format=None):
        ci = self.request.query_params.get('ci') 
        try:
            Trabajador.objects.get(ci=ci) # retrieve the user using username
        except Trabajador.DoesNotExist:
            return Response("true") # return false as user does not exist
        else:
            return Response("Cedula ya registrada.")


class ValidarCliente(APIView):
    def get(self, request, format=None):
        rif = self.request.query_params.get('rif') 
        try:
            Cliente.objects.get(rif=rif) # retrieve the user using username
        except Cliente.DoesNotExist:
            return Response("true") # return false as user does not exist
        else:
            return Response("Rif ya registrado")


class ValidarServicio(APIView):
    def get(self, request, format=None):
        codigo = self.request.query_params.get('codigo') 
        try:
            Servicio.objects.get(codigo=codigo) # retrieve the user using username
        except Servicio.DoesNotExist:
            return Response("true") # return false as user does not exist
        else:
            return Response("Codigo servicio ya registrado")


class CurrentUser(APIView):

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserSerializer(request.user)
        
        try:
            if (request.user.is_superuser):
                data = {}
                data['cargo'] = "admin"
                return Response(data,status=status.HTTP_200_OK)
            else:
                user = Trabajador.objects.get(usuario=serializer.data['id'])
                serialized = TrabajadorSerializer(user)
                return Response(serialized.data, status=status.HTTP_200_OK)
        except Trabajador.DoesNotExist:
            return Response("No existe el trabajador", status=status.HTTP_404_NOT_FOUND)