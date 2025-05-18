from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Trivia
from ..serializers import AdminTriviaSerializer
from ..permissions import IsAdminUserRole
from drf_spectacular.utils import extend_schema

@extend_schema(
    summary="CRUD de Trivias para Administradores",
    description="Permite a los administradores crear, listar, actualizar y eliminar trivias.",
    tags=["Admin Trivias"]
)
class AdminTriviaViewSet(viewsets.ModelViewSet):
    """
    Vista para que los administradores creen y gestionen trivias.
    """
    queryset = Trivia.objects.all()
    serializer_class = AdminTriviaSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]