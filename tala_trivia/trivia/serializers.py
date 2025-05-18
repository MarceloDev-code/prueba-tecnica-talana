from rest_framework import serializers
from .models import User, Question, Option, Trivia, UserAnswer
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'role']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user



class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'difficulty', 'options']

    def create(self, validated_data):
        options_data = validated_data.pop('options')
        question = Question.objects.create(**validated_data)
        for option in options_data:
            Option.objects.create(question=question, **option)
        return question
    

class TriviaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trivia
        fields = ['id', 'name', 'description', 'questions', 'users']


class OptionSubmitSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    option_id = serializers.IntegerField()


class SubmitTriviaSerializer(serializers.Serializer):
    answers = OptionSubmitSerializer(many=True)


class TriviaQuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text']


class TriviaQuestionSerializer(serializers.ModelSerializer):
    options = TriviaQuestionOptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'options']


class AdminTriviaSerializer(serializers.ModelSerializer):
    questions = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), many=True)
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = Trivia
        fields = ['id', 'name', 'description', 'questions', 'users']


class BulkOptionSerializer(serializers.Serializer):
    text = serializers.CharField()
    is_correct = serializers.BooleanField()

class BulkQuestionSerializer(serializers.Serializer):
    text = serializers.CharField()
    difficulty = serializers.ChoiceField(choices=Question.DIFFICULTY_CHOICES)
    options = BulkOptionSerializer(many=True)

class BulkCreateQuestionsSerializer(serializers.Serializer):
    trivia_id = serializers.IntegerField()
    questions = BulkQuestionSerializer(many=True)
    def validate_questions(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("Se requiere al menos una pregunta.")
        return value


class UserTriviaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trivia
        fields = ['id', 'name', 'description']


class TriviaRankingSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    score = serializers.IntegerField()
    correct_answers = serializers.IntegerField()
    total_answers = serializers.IntegerField()