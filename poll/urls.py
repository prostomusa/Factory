from django.urls import re_path, path, include
from .views import *
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('poll/answer/<int:id_poll>/<int:id_user>', answer_question),
    path('poll/<int:id_poll>/get_question', get_question),
    path('poll/question/<int:id_question>', question),
    path('poll/<int:id_poll>/question', question_create),
    path('poll/user/<int:id_user>', get_polls),
    path('poll/<int:id_poll>/', poll),
    path('poll/create/', polls_create),
    path('poll/list/', polls_list),
    path('login', obtain_auth_token, name="login"),
    #path('profile/create/', ProfileCreateView.as_view()),
    #path('client/create/', ClientCreateView.as_view())
]
