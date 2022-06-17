from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=255,blank=True)

    class Meta:
        db_table = "organization"


class Profile(models.Model):
    guid = models.CharField(max_length=255, blank=True)
    full_name = models.CharField(max_length=255, blank=True)
    mobile_phone = models.CharField(max_length=255,blank=True)
    birth = models.DateField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING)
    subdivision = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "profile"


class Test(models.Model):
    name = models.CharField(max_length=255, blank=True)
    type = models.IntegerField(default=0)  # 1 - совпадение, 2 - методика
    total = models.IntegerField(blank=False)

    class Meta:
        db_table = "test"


class Interview(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    test = models.ForeignKey(Test, on_delete=models.DO_NOTHING)
    progress = models.IntegerField(default=0)
    attention = models.BooleanField(blank=True)

    class Meta:
        db_table = "interview"


class Questions(models.Model):  # Тексты вопросов
    test = models.ForeignKey(Test, on_delete=models.DO_NOTHING)
    number = models.IntegerField(blank=False)
    text = models.TextField(max_length=255, blank=True)
    answer_group = models.IntegerField(blank=False)

    class Meta:
        db_table = "questions"


class Answers(models.Model):
    group = models.IntegerField(blank=False)
    number = models.IntegerField(blank=False)
    text = models.TextField(max_length=255, blank=True)

    class Meta:
        db_table = "answers"


class Methodology(models.Model):  # Методика оценки
    test = models.ForeignKey(Test, on_delete=models.DO_NOTHING)
    number = models.IntegerField(blank=False)
    value = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "methodology"


class Choices(models.Model):  # Ответы, выбранные пользователем в конкретном тесте
    interview = models.ForeignKey(Interview, on_delete=models.DO_NOTHING)
    number = models.IntegerField(blank=False)
    value = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "choices"
