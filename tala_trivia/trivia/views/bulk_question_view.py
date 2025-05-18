from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from ..models import Trivia, Question, Option
from ..serializers import BulkCreateQuestionsSerializer

class BulkQuestionCreateView(APIView):
    """
    Crea múltiples preguntas con opciones y las asigna a una trivia.
    """
    serializer_class = BulkCreateQuestionsSerializer
    @extend_schema(
        request=BulkCreateQuestionsSerializer,
        summary="Crear múltiples preguntas",
        description="Recibe un listado de preguntas con opciones y las asigna a una trivia existente."
    )
    def post(self, request):
        serializer = BulkCreateQuestionsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        trivia_id = serializer.validated_data['trivia_id']
        questions_data = serializer.validated_data['questions']

        try:
            trivia = Trivia.objects.get(id=trivia_id)
        except Trivia.DoesNotExist:
            return Response({"error": "Trivia no encontrada."}, status=404)

        created_questions = []

        for q_data in questions_data:
            options_data = q_data.pop('options')
            question = Question.objects.create(**q_data)
            for opt_data in options_data:
                Option.objects.create(question=question, **opt_data)
            trivia.questions.add(question)
            created_questions.append(question.text)

        return Response({
            "message": f"{len(created_questions)} preguntas creadas y asignadas a la trivia '{trivia.name}'.",
            "created_questions": created_questions
        }, status=status.HTTP_201_CREATED)
