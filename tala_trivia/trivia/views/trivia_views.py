from rest_framework import viewsets
from ..models import Trivia
from ..serializers import TriviaSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(
    summary="CRUD de Trivias",
    description="Permite crear, listar, actualizar y eliminar trivias.",
    tags=["Trivias"]
)
class TriviaViewSet(viewsets.ModelViewSet):
    queryset = Trivia.objects.all()
    serializer_class = TriviaSerializer
