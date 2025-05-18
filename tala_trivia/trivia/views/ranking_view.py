from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from ..models import Trivia, UserAnswer
from ..serializers import TriviaRankingSerializer

from ..constants import SCORES_BY_DIFFICULTY
from drf_spectacular.utils import extend_schema

@extend_schema(
    summary="Ranking de Trivia",
    description="Obtiene el ranking de usuarios por puntaje en una trivia específica.",
)
class TriviaRankingView(APIView):
    """
    Retorna el ranking de usuarios por puntaje en una trivia.
    """

    def get(self, request, trivia_id):
        trivia = get_object_or_404(Trivia, id=trivia_id)
        answers = UserAnswer.objects.filter(trivia=trivia).select_related('question', 'user')

        ranking = {}
        for answer in answers:
            user_id = answer.user.id
            username = answer.user.username
            is_correct = answer.is_correct
            difficulty = answer.question.difficulty
            score = SCORES_BY_DIFFICULTY.get(difficulty, 0) if is_correct else 0

            if user_id not in ranking:
                ranking[user_id] = {
                    'user_id': user_id,
                    'username': username,
                    'score': 0,
                    'correct_answers': 0,
                    'total_answers': 0
                }

            ranking[user_id]['score'] += score
            ranking[user_id]['correct_answers'] += int(is_correct)
            ranking[user_id]['total_answers'] += 1

        sorted_ranking = sorted(ranking.values(), key=lambda x: x['score'], reverse=True)

        serializer = TriviaRankingSerializer(sorted_ranking, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
