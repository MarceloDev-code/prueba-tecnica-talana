from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.user_views import UserViewSet, UserTriviasView
from .views.question_views import QuestionViewSet
from .views.trivia_views import TriviaViewSet
from .views.answer_view import QuizzView
from .views.admin_views import AdminTriviaViewSet
from .views.bulk_question_view import BulkQuestionCreateView
from .views.ranking_view import TriviaRankingView


router = DefaultRouter()
router.register('users', UserViewSet)
router.register('questions', QuestionViewSet)
router.register('trivias', TriviaViewSet)
router.register('admin/trivias', AdminTriviaViewSet, basename='admin-trivias')

urlpatterns = [
    path('', include(router.urls)),
    path('trivias/<int:trivia_id>/play/<int:user_id>/', QuizzView.as_view(), name='quizz-view'),
    path('admin/questions/bulk/', BulkQuestionCreateView.as_view(), name='bulk-question-create'),
    path('users/<int:user_id>/trivias/', UserTriviasView.as_view(), name='user-trivias'),
    path('trivias/<int:trivia_id>/ranking/', TriviaRankingView.as_view(), name='trivia-ranking'),


]
