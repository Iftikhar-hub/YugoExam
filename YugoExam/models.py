# models.py
from django.contrib.auth.models import Group, Permission
from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User


# Semester choices
SEMESTER_CHOICES = [
    ('1st', '1st Semester'),
    ('2nd', '2nd Semester'),
    ('3rd', '3rd Semester'),
    ('4th', '4th Semester'),
    ('5th', '5th Semester'),
    ('6th', '6th Semester'),
    ('7th', '7th Semester'),
    ('8th', '8th Semester'),
]

class Department(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='subjects')
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES,default='1st' )
    def __str__(self):
        return f"{self.name} ({self.department.name} - {self.semester})"

class Teacher(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True, null=True)
    qualification = models.CharField(max_length=200, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)  # Gender field
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    subjects = models.ManyToManyField(Subject,  related_name='teachers', blank=True)  # Many-to-many relationship
    is_staff = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='teacher_images/', blank=True, null=True)
    def __str__(self):
        return self.email

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,default=1)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL,related_name="students", null=True, blank=True)
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES,default='1st')
    subjects = models.ManyToManyField(Subject,related_name="students", blank=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], blank=True, null=True)
    profile_picture = models.ImageField(upload_to='student_images/', blank=True, null=True)
    is_staff = models.BooleanField(default=False)

  
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.email
    
class Exam(models.Model):
    EXAM_TYPES = [
        ('MC', 'Multiple Choice'),
        ('ST', 'Subjective'),
        ('SE', 'Short Easy'),
    ]

    exam_title = models.CharField(max_length=200)
    exam_type = models.CharField(max_length=2, choices=EXAM_TYPES, default='MC')  # Default to Multiple Choice
    schedule = models.DateTimeField()
    total_marks = models.PositiveIntegerField()
    passing_marks = models.PositiveIntegerField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    published = models.BooleanField(default=False)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.exam_title} - {self.get_exam_type_display()}"    

class Question(models.Model):
    exam = models.ForeignKey('Exam', on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()  
    option_a = models.CharField(max_length=255)  
    option_b = models.CharField(max_length=255)  
    option_c = models.CharField(max_length=255)  
    option_d = models.CharField(max_length=255)  
    correct_option = models.IntegerField(choices=[(1, 'Option a'), (2, 'Option b'), (3, 'Option c'), (4, 'Option d')]) 
    marks = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.question_text


class SubjectiveQuestion(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='subjective_question')
    question_text = models.TextField()
    reference_answer = models.TextField(default="")
    STmarks = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.question_text
    
class SubjectiveAnswer(models.Model):
    question = models.ForeignKey(SubjectiveQuestion, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='subjective_answers') 
    student_answer = models.TextField()
    marks_awarded = models.FloatField()

    def __str__(self):
        return f"{self.student.username} answer for {self.question} - Marks: {self.marks_awarded}"



class StudentExam(models.Model):
    STATUS_CHOICES = [
        ('taken', 'Taken'),
        ('pending', 'Pending'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_exams')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='student_exams')
    subject = models.CharField(max_length=255,  default="Default Exam Subject")
    exam_title = models.CharField(max_length=255, default="Default Exam Title")
    total_marks = models.PositiveIntegerField(default=0)
    obtained_marks = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='taken')

    def __str__(self):
        return f"{self.student.username} - {self.exam_title}"
