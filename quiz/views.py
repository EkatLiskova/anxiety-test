from django.shortcuts import render, redirect
from rest_framework.response import Response
from django.template import loader
from django.http import JsonResponse, HttpResponseRedirect
from rest_framework.views import APIView

from .models import Test, Questions, Answers, Interview, Choices, Methodology


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
    data_set = []
    tests = Test.objects.all()
    for test in tests:
        try:
            interview = Interview.objects.get(test_id=test.id, profile_id=1)
            total_progress = float(interview.progress)/float(test.total)
            if interview.progress == 1:
                progress_status = "Тест не начат"
            elif total_progress > 1:
                progress_status = "Тест завершён"
            else:
                progress_status = "Прогресс теста: ("+str(interview.progress)+"/"+str(test.total)+")"
        except:
            progress_status = "Тест на стадии разработки"

        data_set.append({"id": test.id, "name": test.name, "progress": progress_status})


    # interview = Interview.objects.get(test_id=1, profile_id=1)
    # current_question = interview.progress
    # data_set = [{"id": x.id, "name": x.name} for x in tests]
    return render(request, 'profile.html', context={'data_set': data_set})

def quiz(request):
    test = Test.objects.get(id=1)
    interview = Interview.objects.get(test_id=test.id, profile_id=1)
    current_question = interview.progress
    if current_question > test.total:
        return HttpResponseRedirect("/result/")
    else:
        question = Questions.objects.get(test_id=test.id, number=current_question)
        answers_queryset = Answers.objects.filter(group=question.answer_group)
        answers = [{"number": x.number, "text": x.text} for x in answers_queryset]
        data_set = {"progress_bar": "Утверждение ("+str(current_question)+"/"+str(test.total)+"): ",
                    "question": question.text, "answers": answers}
        # print(data_set)
        return render(request, 'quiz.html', context={'data_set': data_set})


def write_choise(request):
    if request.method == "POST":
        test = Test.objects.get(id=1)
        interview = Interview.objects.get(test_id=test.id, profile_id=1)
        current_question = interview.progress
        try:
            if request.POST.get("answer1"):
                Choices.objects.create(number=current_question,interview_id=interview.id,value=1)
            elif request.POST.get("answer2"):
                Choices.objects.create(number=current_question,interview_id=interview.id,value=2)
            elif request.POST.get("answer3"):
                Choices.objects.create(number=current_question,interview_id=interview.id,value=3)
            elif request.POST.get("answer4"):
                Choices.objects.create(number=current_question,interview_id=interview.id,value=4)
            elif request.POST.get("home"):
                return HttpResponseRedirect("/profile/1/")
            elif request.POST.get("clear"):
                interview.progress = 1
                interview.save()
                Choices.objects.filter(interview_id=interview.id).delete()
                return HttpResponseRedirect("/profile/1")
        except:
            print("value already exist")

        print(interview.progress)
        interview.progress += 1
        interview.save()
        print(interview.progress)


        if interview.progress > test.total:
            return HttpResponseRedirect("/result/")
        else:
            return HttpResponseRedirect("/quiz/")


def result(request):

    """
    - до 30 баллов – тревожность отсутствует;
- от 31 до 44 баллов – умеренная тревожность;
- 45 и более – выраженная тревожность.

    """


    test = Test.objects.get(id=1)
    result_sum = 0

    quiz = Interview.objects.get(profile=1, test_id=test.id)
    choices = Choices.objects.filter(interview=quiz)
    for choice in choices:
        choice_value = int(choice.value)
        str_points = Methodology.objects.get(test_id=test.id, number=choice.number).value
        result_sum += int(str_points[choice_value-1])
    if result_sum<15:
        result_text="тревожность отсутствует"
    elif result_sum>23:
        result_text = "выраженная тревожность"
    else:
        result_text = "умеренная тревожность"

    return render(request, 'result.html', context={'data_set': result_text})
