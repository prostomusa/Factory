from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)
# Create your models here.

class Polls(models.Model):
	name = models.CharField(max_length=50)
	date_start = models.DateTimeField(auto_now_add=True)
	date_end = models.DateTimeField(null=True)
	description = models.CharField(max_length=150)

class Question(models.Model):
	poll = models.ForeignKey(Polls, on_delete = models.CASCADE, related_name='pl')
	question = models.CharField(max_length=50, unique=True)
	type_questions = (
		(1, "Ответ текстом"),
		(2, "Ответ с одним вариантом ответа"),
		(3, "Ответ с несколькими вариантами ответа"),
	)
	t_question = models.IntegerField(choices=type_questions)

class Answer(models.Model):
	question = models.ForeignKey(Question, on_delete = models.CASCADE, related_name='qs')
	answer = models.CharField(max_length=50)

class Profile(models.Model):
	polls = models.ManyToManyField(Polls)
	answer = models.ManyToManyField(Answer)

