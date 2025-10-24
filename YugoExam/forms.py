from django import forms
from .models import Exam, Question, Teacher, Student, Subject, Department
from django.contrib.auth.hashers import make_password 
from .models import SubjectiveQuestion
from django.contrib.auth.models import User


class TeacherRegistrationForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'phone', 'qualification', 'subjects', 'department', 'gender', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match')
        return cleaned_data

    def save(self, commit=True):
        teacher = super().save(commit=False)
        user = User.objects.create_user(
            username=self.cleaned_data['email'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        teacher.user = user
        if commit:
            teacher.save()
            self.save_m2m()
        return teacher

class StudentRegistrationForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'phone', 'department', 'semester', 'subjects', 'gender', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'semester': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'subjects': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subjects'].queryset = Subject.objects.none()

        if 'department' in self.data and 'semester' in self.data:
            try:
                department_id = int(self.data.get('department'))
                semester = self.data.get('semester')
                self.fields['subjects'].queryset = Subject.objects.filter(department_id=department_id, semester=semester)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.department:
            self.fields['subjects'].queryset = self.instance.department.subjects.filter(semester=self.instance.semester)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        student = super().save(commit=False)
        user = User.objects.create_user(
            username=self.cleaned_data['email'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        student.user = user
        if commit:
            student.save()
            self.save_m2m()
        return student
    
class MultipleChoiceExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['exam_title', 'exam_type', 'schedule', 'total_marks', 'passing_marks', 'subject']
        widgets = {
            'exam_title': forms.TextInput(attrs={'class': 'form-control'}),
            'schedule': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'total_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'passing_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        teacher_subjects = kwargs.pop('teacher_subjects', None)
        super(MultipleChoiceExamForm, self).__init__(*args, **kwargs)
        if teacher_subjects:
            self.fields['subject'].queryset = teacher_subjects

class SubjectiveExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['exam_title', 'exam_type', 'schedule', 'total_marks', 'passing_marks', 'subject']
        widgets = {
            'exam_title': forms.TextInput(attrs={'class': 'form-control'}),
            'schedule': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'total_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'passing_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        teacher_subjects = kwargs.pop('teacher_subjects', None)
        super(SubjectiveExamForm, self).__init__(*args, **kwargs)
        if teacher_subjects:
            self.fields['subject'].queryset = teacher_subjects

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_option'] 
        widgets = {
            'question_text': forms.TextInput(attrs={'class': 'form-control custom-class'}),
            'option_a': forms.TextInput(attrs={'class': 'form-control'}),
            'option_b': forms.TextInput(attrs={'class': 'form-control'}),
            'option_c': forms.TextInput(attrs={'class': 'form-control'}),
            'option_d': forms.TextInput(attrs={'class': 'form-control'}),
            'correct_option': forms.Select(attrs={'class': 'form-control'}),
            'correct_option': forms.Select(attrs={'class': 'form-control'}),
        }
        

class SubjectiveQuestionForm(forms.ModelForm):
    class Meta:
        model = SubjectiveQuestion
        fields = ['question_text', 'STmarks','reference_answer']
        widgets = {
            'question_text': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
            'reference_answer': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
            'STmarks': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ShortEssayExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['exam_title', 'exam_type', 'schedule', 'total_marks', 'passing_marks', 'subject']
        widgets = {
            'exam_title': forms.TextInput(attrs={'class': 'form-control'}),
            'schedule': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'total_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'passing_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        teacher_subjects = kwargs.pop('teacher_subjects', None)
        super(ShortEssayExamForm, self).__init__(*args, **kwargs)
        if teacher_subjects:
            self.fields['subject'].queryset = teacher_subjects


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'phone', 'gender', 'department', 'semester', 'subjects', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super(StudentProfileForm, self).__init__(*args, **kwargs)

        # Ensure instance exists
        if self.instance and self.instance.semester and self.instance.department:
            self.fields['subjects'].queryset = Subject.objects.filter(
                semester=self.instance.semester,
                department=self.instance.department
            )
        else:
            # Fallback to no subjects
            self.fields['subjects'].queryset = Subject.objects.none()

        # Optional: Improve widget appearance
        self.fields['subjects'].widget.attrs.update({'class': 'subject-select'})
