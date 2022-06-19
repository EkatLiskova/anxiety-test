"""psychological_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from quiz.views import quiz, login, home, profile, write_choise, result

urlpatterns = [
    path('', home),
    path('profile/1/', profile, name="profile"),
    path('login/', login, name="login"),
    path('admin/', admin.site.urls),
    path('quiz/', quiz, name="quiz"),
    path('quiz/write_choise/', write_choise, name="write_choise"),
    path('result/', result, name="result")

]
