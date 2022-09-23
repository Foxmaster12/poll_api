from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Poll(models.Model):
    poll_name = models.CharField(max_length=50)
    poll_start = models.DateTimeField(default=timezone.now)
    poll_finish = models.DateTimeField()
    description = models.TextField()

    def __str__(self):
        return self.poll_name

    def clean(self):
        if self.poll_start >= self.poll_finish:
            raise ValidationError("Incorrect finish date: the date must be later than start date")


class Question(models.Model):
    MANY = 'Many'
    ONE_CHOICE = 'One'
    TEXT = 'Text'
    QUESTION_TYPE_CHOICES = [
        (MANY, 'With many choices'),
        (ONE_CHOICE, 'With one choice'),
        (TEXT, 'With text answer')
    ]
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE)
    question_type = models.CharField(choices=QUESTION_TYPE_CHOICES, max_length=30)
    question_text = models.TextField()

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=20)


class UserAnswer(models.Model):
    user_name = models.CharField(max_length=255)
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
