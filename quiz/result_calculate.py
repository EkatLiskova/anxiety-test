from .models import Test, Interview, Choices, Methodology


class Interpretation:

    @staticmethod
    def result_calculate(user_id, test_id):
        result_sum = 0
        quiz = Interview.objects.get(profile=user_id, test=test_id)
        choices = Choices.objects.filter(interview=quiz)
        for choice in choices:
            choice_value = int(choice.value)
            str_points = Methodology.objects.get(test=test_id, number=choice.number).value
            result_sum += int(str_points[choice_value])
        return result_sum





