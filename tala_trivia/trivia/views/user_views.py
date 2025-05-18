from rest_framework import viewsets
from ..models import User
from ..serializers import UserSerializer, UserTriviaListSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsAdminUserRole
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema


@extend_schema(
    summary="CRUD de Usuarios",
    description="Permite crear, listar, actualizar y eliminar usuarios.",
    tags=["Usuarios"]
)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]

@extend_schema(
    summary="Trivias de Usuario",
    description="Lista todas las trivias asignadas a un usuario.",
    tags=["Usuarios"]
)
class UserTriviasView(APIView):
    """
    Lista todas las trivias asignadas a un usuario.
    """
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        trivias = user.trivias.all()
        serializer = UserTriviaListSerializer(trivias, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)