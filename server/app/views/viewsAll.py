from django.contrib.auth.models import User
from app.models import Trabajador
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


def viewsTodos(arg):
    pass


class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data['user'])
        if serializer.is_valid():
            user = User.objects.create_user(
                serializer.validated_data['username'],
                serializer.validated_data['email'],
                serializer.validated_data['password']
            )
            request.data['trabajador']['usuario'] = user.pk
            serializer1 = TrabajadorSerializer(data=request.data['trabajador'])
            if serializer1.is_valid():
                serializer1.save()
                return Response(serializer1.data, status=status.HTTP_201_CREATED)
            else:
                instance = User.objects.get(id= user.pk)
                instance.delete()
                return Response(serializer1.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ValidarUsuario(APIView):
    def get(self, request, format=None):
        username = self.request.query_params.get('username')
        print(username)
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

class CurrentUser(APIView):

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserSerializer(request.user)
        user = Trabajador.objects.get(usuario=serializer.data['id'])
        serialized = TrabajadorSerializer(user)
        return Response(serialized.data)