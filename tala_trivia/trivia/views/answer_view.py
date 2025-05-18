from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from rest_framework.permissions import IsAuthenticated

from ..models import Trivia, Question, Option, UserAnswer
from ..serializers import (
    SubmitTriviaSerializer,
    TriviaQuestionSerializer
)
from ..constants import SCORES_BY_DIFFICULTY

class QuizzView(APIView):
    """
    GET: Obtener las preguntas de una trivia asignada (sin mostrar respuestas correctas)
    POST: Enviar respuestas, calcular puntaje, y registrar resultados
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, trivia_id, user_id):
        trivia = get_object_or_404(Trivia, id=trivia_id)
        if not trivia.users.filter(id=user_id).exists():
            return Response({'detail': 'Este usuario no está asignado a esta trivia.'}, status=403)

        questions = trivia.questions.all()
        serializer = TriviaQuestionSerializer(questions, many=True)
        return Response({'trivia': trivia.name, 'questions': serializer.data})
    @extend_schema(
    request=SubmitTriviaSerializer,
    summary="Enviar respuestas de trivia",
    description="Recibe respuestas de un usuario para una trivia y devuelve el puntaje."
    )
    def post(self, request, trivia_id, user_id):
        trivia = get_object_or_404(Trivia, id=trivia_id)
        if not trivia.users.filter(id=user_id).exists():
            return Response({'detail': 'Este usuario no está asignado a esta trivia.'}, status=403)

        serializer = SubmitTriviaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        answers_data = serializer.validated_data['answers']
        total_score = 0
        results = []

        for answer in answers_data:
            question_id = answer['question_id']
            option_id = answer['option_id']

            question = get_object_or_404(Question, id=question_id)
            selected_option = get_object_or_404(Option, id=option_id, question=question)

            is_correct = selected_option.is_correct
            score = SCORES_BY_DIFFICULTY.get(question.difficulty, 0) if is_correct else 0
            total_score += score

            UserAnswer.objects.update_or_create(
                user_id=user_id,
                trivia_id=trivia_id,
                question=question,
                defaults={
                    'selected_option': selected_option,
                    'is_correct': is_correct
                }
            )

            results.append({
                'question': question.text,
                'correct': is_correct,
                'points_awarded': score
            })

        return Response({
            'total_score': total_score,
            'details': results
        }, status=status.HTTP_200_OK)
