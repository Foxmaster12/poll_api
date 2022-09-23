from rest_framework import serializers
from .models import Poll, Choice, Question, UserAnswer


class PollSerializer(serializers.ModelSerializer):
    style = {'base_template': 'poll/poll.html'}

    class Meta:
        model = Poll
        fields = ['pk', 'poll_name', 'poll_finish']


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['answer_text', ]


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, source='choice_set')

    class Meta:
        model = Question
        fields = ['question_text', 'question_type', 'choices', 'pk']


class UserAnswerSerializer(serializers.ModelSerializer):

    poll = PollSerializer()

    class Meta:
        model = UserAnswer
        fields = ['pk', 'poll', 'question', 'answer', 'user_name']
