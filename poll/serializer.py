from rest_framework import serializers
from .models import *

class QuestionDisplaySerializer(serializers.ModelSerializer):
    type_of_question = serializers.CharField(source='get_t_question_display')
    class Meta:
        model = Question
        fields = ['id', 'question', 'type_of_question']

class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['question', 't_question']

class AnswerQuestionSerializer(serializers.ModelSerializer):
    question = serializers.CharField()#source='ans')
    class Meta:
        model = Answer
        fields = ['question', 'answer']

class PollsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Polls
        fields = ['id', 'name', 'description']

class PollsSerializer(serializers.ModelSerializer):
    poll = QuestionDisplaySerializer(source='pl', many=True)
    class Meta:
        model = Polls
        fields = ['id', 'name', 'description', 'poll']


