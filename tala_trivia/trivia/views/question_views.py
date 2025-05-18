from rest_framework import viewsets
from ..models import Question
from ..serializers import QuestionSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(
    summary="CRUD de Preguntas",
    description="Permite crear, listar, actualizar y eliminar preguntas.",
    tags=["Preguntas"]
)
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
