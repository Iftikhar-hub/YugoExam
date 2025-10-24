from django import template

register = template.Library()

@register.filter
def get_total_time(question_count):
    time_per_question = 60  # 1 minute per question
    return question_count * time_per_question
