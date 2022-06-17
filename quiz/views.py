from django.shortcuts import render, redirect
from rest_framework.response import Response
from django.template import loader
from django.http import JsonResponse, HttpResponseRedirect
from rest_framework.views import APIView

from .models import Test, Questions, Answers


class QuizList(APIView):
    def get(self, request):
        tests = Test.objects.all()
        data_set = {"tests": [{"id": x.id, "name": x.name} for x in tests]}
        return JsonResponse(data_set, status=200)


class AnswerWizard(APIView):
    def get(self, request, q_id):
        test = Test.objects.get(id=1)
        question = Questions.objects.get(number=q_id, test_id=test.id)
        answers_queryset = Answers.objects.filter(group=question.answer_group)
        answers = [{"number": x.number, "text": x.text} for x in answers_queryset]
        data_set = {"question": question.text, "answers": answers}
        return JsonResponse(data_set, status=200)


def login(request):
    return render(request, 'login.html')

def home(request):
    return HttpResponseRedirect('login/')

def profile(request):
    return render(request, 'profile.html')
