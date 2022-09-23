from django.urls import path
from poll.views import *

urlpatterns = [
    path('poll_list/', PollListView.as_view()),
    path('poll/<int:pk>/', PassPollView.as_view()),
    path('poll/<int:pk>/anon/', PassPollAnon.as_view()),
    path('get_passed/', GetPassedPollView.as_view())

]
