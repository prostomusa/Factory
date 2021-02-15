from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics
from django.http import HttpResponse, JsonResponse, HttpRequest
from .serializer import *
from .models import *
import json
from datetime import datetime
#from account.api.serializers import RegistrationSerializer

# Create your views here.
class PollsCreateView(generics.CreateAPIView):
    serializer_class = AnswerQuestionSerializer

@api_view(['GET', ])
def polls_list(request: HttpRequest) -> HttpResponse:
	list_polls = []
	polls = Polls.objects.all()
	if request.method == "GET":
		for i in polls:
			dicti = {}
			serializer = PollsSerializer(i)
			dicti['ID Опроса'] = serializer.data['id']
			dicti['Название опроса'] = serializer.data['name']
			dicti['Описание'] = serializer.data['description']
			dicti['Вопросы'] = serializer.data['poll']
			list_polls.append(dicti)
		return Response(json.loads(json.dumps(list_polls)))

@api_view(['GET'])
def get_question(request: HttpRequest, id_poll: int) -> HttpResponse:
	dicti = {}
	try:
		polls = Polls.objects.get(id=id_poll)
	except Polls.DoesNotExist:
		return JsonResponse({'Опрос':'Опроса с таким ID не существует'})

	if request.method == "GET":
		mass = []
		questions = polls.pl.all()
		for i in questions:
			print(i.question)
			dicti['question'] = i.question
			dicti['answer'] = "" 
			mass.append(dicti.copy())
		return Response(json.loads(json.dumps(mass)))

@api_view(['POST'])
def answer_question(request: HttpRequest,\
					id_poll: int, id_user: int) -> HttpResponse:
	try:
	    polls = Polls.objects.get(id=id_poll)
	    useranswer = Profile.objects.get(id=id_user,polls=polls)
	    user = Profile.objects.filter(id=id_user, polls=polls)
	    if len(user) > 0:
	        return Response('Вы уже проходили этот опрос')
	    else:
	        useranswer.polls.add(polls)
	except Profile.DoesNotExist:
	    useranswer = Profile(id=id_user)
	    useranswer.save()
	    useranswer.polls.add(polls)
	    #useranswer.save()
	except Polls.DoesNotExist:
	    return JsonResponse({'Опрос':'Опроса с таким ID не существует'})

	if request.method == "POST":
		polls = useranswer.polls.get(id=id_poll)
		for i in request.data:
			quest = Question.objects.get(poll=polls, question=i['question'])
			temp = Answer(question=quest, answer=i['answer'])
			temp.save()
			serializer = AnswerQuestionSerializer(temp, data=i)
			if serializer.is_valid():
				useranswer.answer.add(temp)
			else:
				useranswer.polls.remove(polls)
				temp.delete()
				return Response('Вы неправильно ввели данные')
		polls.date_end = datetime.now()
		polls.save()
		return Response("Спасибо за прохождение опроса")
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_polls(request: HttpRequest, id_user: int) -> HttpResponse:
	try:
	    useranswer = Profile.objects.get(id=id_user)
	except Profile.DoesNotExist:
	    return Response('User с таким ID не существует')
	if request.method == "GET":
		mina = useranswer.polls.all()
		datas = []
		datas1 = []
		answers = []
		k = 0
		t = 0
		for i in mina:
			tr = useranswer.polls.get(id=i.id)
			datas.append({'ID': i.id, 'Начало': i.date_start, 'Окончание': i.date_end, 'Название опроса': i.name})
			question = tr.pl.all()
			answers = useranswer.answer.all()
			if len(question) < 1:
				datas[k]['Ваши вопросы и ответы'] = []
			else:
				for l in range(len(question)):
					datas1.append({'Вопрос': question[l].question, 'Ответ': answers[t].answer})
					t += 1
				datas[k]['Ваши вопросы и ответы'] = datas1[:]
				datas1 = []
				k += 1
	return Response(datas)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def polls_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        dicti = {}
        serializer = PollsCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Вы создали опрос с названием - {}'.format(request.data['name']))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def poll(request: HttpRequest, id_poll: int) -> HttpResponse:
    try:
        polls = Polls.objects.get(id=id_poll)
    except Polls.DoesNotExist:
        return JsonResponse({'Опрос':'Опроса с таким ID не существует'})

    if request.method == 'DELETE':
        name = polls.name
        polls.delete()
        return Response({'Опрос с названием {} был удален'.format(name)})

    elif request.method == 'PUT':
        serializer = PollsSerializer(polls, data=request.data, partial=True)
        dicti = {}
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def question_create(request: HttpRequest, id_poll: int) -> HttpResponse:
	try:
	    polls = Polls.objects.get(id=id_poll)
	except Polls.DoesNotExist:
	    return JsonResponse({'Опрос':'Опроса с таким ID не существует'})
	if request.method == "POST":
		data = []
		for i in request.data:
			print(i['question'])
			temp = Question(poll=polls, question=i['question'], t_question=i['t_question'])
			temp.save()
			serializer = QuestionsSerializer(temp, data=i)
			if serializer.is_valid():
				serializer.save()
				data.append(i['question'])
		return Response(json.loads(json.dumps(data)))
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def question(request: HttpRequest, id_question: int) -> HttpResponse:
    try:
        question = Question.objects.get(id=id_question)
    except Question.DoesNotExist:
        return JsonResponse({'Вопроса':'Вопроса с таким ID не существует'})

    if request.method == "DELETE":
        name = question.question
        question.delete()
        return Response({'Вопрос - ({0}) был удален из опроса'.format(name)})

    elif request.method == "PUT":
        serializer = QuestionsSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
