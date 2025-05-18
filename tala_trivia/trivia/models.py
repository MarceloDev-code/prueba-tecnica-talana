from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=10,
        choices=[("admin", "Admin"), ("player", "Player")],
        default="player"
    )
    mmr = models.IntegerField(default=0)

    def __str__(self):
        return self.username


class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ("easy", "Fácil"),
        ("medium", "Medio"),
        ("hard", "Difícil"),
    ]

    text = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)

    def __str__(self):
        return f"{self.text[:50]}..."


class Option(models.Model):
    question = models.ForeignKey(Question, related_name="options", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} ({'Correcta' if self.is_correct else 'Incorrecta'})"


class Trivia(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    questions = models.ManyToManyField(Question)
    users = models.ManyToManyField(User, related_name="trivias")

    def __str__(self):
        return self.name


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trivia = models.ForeignKey(Trivia, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)
    is_correct = models.BooleanField()

    def __str__(self):
        return f"{self.user.username} - {self.question.text[:30]}"

    class Meta:
        unique_together = ('user', 'trivia', 'question')
