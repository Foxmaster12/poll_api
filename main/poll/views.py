import datetime

from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Poll, Question, UserAnswer
from .serializers import PollSerializer, QuestionSerializer, UserAnswerSerializer


class PollListView(generics.ListAPIView):
    serializer_class = PollSerializer

    def get_queryset(self):
        return Poll.objects.filter(poll_finish__gte=datetime.datetime.now())

    def get(self, request, *args, **kwargs):
        return Response(PollSerializer(self.get_queryset(), many=True).data)


class PassPollAnon(generics.ListCreateAPIView):

    serializer_class = QuestionSerializer

    def get_queryset(self, **kwargs):
        return Question.objects.filter(poll__pk=kwargs.get('pk', None))

    def get(self, request, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': "There is no poll identifier"})
        try:
            poll = Poll.objects.get(pk=pk)
        except:
            return Response({'error': "There is no such poll"})
        data = QuestionSerializer(self.get_queryset(pk=pk), many=True).data
        return render(request, 'poll/quiz_form.html', {'poll': poll, 'data': data})

    def post(self, request, **kwargs):
        poll = Poll.objects.get(pk=kwargs.get('pk'))
        user_name = request.user
        for question in request.data:
            if question != 'csrfmiddlewaretoken':
                for choice in request.POST.getlist(question):
                    UserAnswer.objects.create(user_name=user_name, poll=poll, question=question, answer=choice)

        return Response({"Success": "yes"})


class PassPollView(PassPollAnon):

    permission_classes = [IsAuthenticated, ]


class GetPassedPollView(generics.ListAPIView):

    serializer_class = UserAnswerSerializer

    def get_queryset(self, **kwargs):
        user_name = kwargs.get('user')
        return UserAnswer.objects.filter(user_name=user_name)

    def get(self, request, **kwargs):
        return Response(UserAnswerSerializer(self.get_queryset(user=request.user), many=True).data)
