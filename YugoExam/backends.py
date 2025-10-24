# backends.py
from django.contrib.auth.backends import BaseBackend
from .models import Student, Teacher
from django.contrib.auth.hashers import check_password 
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            teacher = Teacher.objects.get(user__email=email)
            user = teacher.user 
            if user.check_password(password):
                return user
        except Teacher.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Teacher.objects.get(pk=user_id)
        except Teacher.DoesNotExist:
            return None
        

class StudentBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)
            if user.check_password(password) and hasattr(user, 'student'):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None    
