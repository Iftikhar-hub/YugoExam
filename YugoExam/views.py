# views.py
from django.contrib import messages
from django.contrib.auth.models import User

from datetime import datetime, timezone
from django.utils import timezone
import json

from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, render, redirect

from django.urls import reverse
from django.http import JsonResponse
from YugoExam.backends import StudentBackend
from .models import Department, Student, StudentExam, SubjectiveQuestion, Teacher, Subject
from .forms import MultipleChoiceExamForm, ShortEssayExamForm, StudentRegistrationForm, SubjectiveExamForm, SubjectiveQuestionForm, TeacherRegistrationForm
from django.contrib.auth.hashers import make_password  # Import make_password
from django.http import HttpResponse, JsonResponse  # Import JsonResponse
# from .forms import ExamForm
from .forms import QuestionForm
from .models import Exam, Question
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.template.loader import get_template
from xhtml2pdf import pisa
from sklearn.metrics.pairwise import cosine_similarity 
from sentence_transformers import SentenceTransformer 
from .models import SubjectiveAnswer

from django.db import transaction
 

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.core.exceptions import ObjectDoesNotExist
import spacy 
from .utils import extract_topic_from_question, topic_links
from YugoExam.utils import extract_topic_from_question, topic_links, get_similarity
import difflib
from collections import Counter
from .forms import StudentProfileForm, UserUpdateForm
from .models import SEMESTER_CHOICES
from YugoExam import models
from django.db.models import Avg








def index(request):
    return render(request, 'index.html')

def signup(request):
    return render(request, 'signup.html')


def about(request):
    return render(request, 'about.html')

def teacher_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Get the user object from the email
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            return redirect('teacher_dashboard')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'teacher_login.html')


def teacher_register(request):
    departments = Department.objects.all()

    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            teacher = form.save(commit=False)
            user = teacher.user
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            teacher.save()
            form.save_m2m()
            messages.success(request, 'Registration successful!')
            return redirect('teacher_login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TeacherRegistrationForm()

    context = {
        'departments': departments,
        'form': form,
    }
    return render(request, 'teacher_register.html', context)

def get_subjects_by_department(request):
    department_id = request.GET.get('department_id')
    subjects = Subject.objects.filter(department_id=department_id).values('id', 'name')
    return JsonResponse(list(subjects), safe=False)


def update_subjects(request):
    department_id = request.GET.get('department_id')
    semester = request.GET.get('semester')
    subjects = Subject.objects.filter(department_id=department_id, semester=semester)
    subject_list = [{'id': subject.id, 'name': subject.name} for subject in subjects]
    return JsonResponse({'subjects': subject_list})
def add_department(request):
    if request.method == 'POST':
        new_department = request.POST.get('new_department')
        new_subject = request.POST.get('new_subject')

        if new_department and new_subject:
            # Check if the department already exists
            department, created = Department.objects.get_or_create(name=new_department)
            
            # Add the subject to the department (whether it's new or existing)
            subject_exists = Subject.objects.filter(name=new_subject, department=department).exists()
            
            if not subject_exists:
                subject = Subject.objects.create(name=new_subject, department=department)
                return JsonResponse({'success': True, 'message': 'Subject added successfully'})
            else:
                return JsonResponse({'success': False, 'message': 'Subject already exists in this department'})
        else:
            return JsonResponse({'success': False, 'message': 'Please fill out both fields'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})

def student_dashboard(request):
    student = Student.objects.get(user=request.user)
    subject = student.subjects.all()
    semester=student.semester
    total_courses = student.subjects.count()
    upcoming_exams = Exam.objects.filter(published=True, schedule__gt=datetime.now())
    available_subjects = Subject.objects.filter(department=student.department,semester=student.semester).exclude(id__in=student.subjects.values_list('id', flat=True))


    if request.method == 'POST':
     id = request.POST.get('subject')
     selected_course = Subject.objects.get(id=id)
     student.subjects.add(selected_course)  # Enroll the student
     return redirect('student_dashboard')
    
    student_department = student.department
    exams = Exam.objects.filter(subject__department=student_department)
    now = timezone.now()
     # Check if the student has taken any exam
    for exam in exams:
        exam.is_taken = exam.student_exams.filter(student=student, status='taken').exists()

        
    context = {
        'total_courses': total_courses,
        'upcoming_exams': upcoming_exams,
        'subjects' : subject,
        'semester' : semester,
        'available_subjects': available_subjects,
        'exams': exams,
        'now': now,
        
    }
    return render(request, 'student_dashboard.html', context)


def student_register(request):
    departments = Department.objects.all()

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # The form handles user creation and linking internally
            messages.success(request, 'Registration successful!')
            return redirect('student_login')
        else:
            print("Form errors:", form.errors)
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentRegistrationForm()

    context = {
        'departments': departments,
        'form': form,
    }
    return render(request, 'student_register.html', context)

def student_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('student_dashboard')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'student_login.html')

def teacher_dashboard(request):
    teacher = Teacher.objects.get(user=request.user)  # Assuming the teacher is logged in  
    selected_semester = request.GET.get('semester')  # Get semester from query parameters
    teacher_subjects = Subject.objects.filter(department=teacher.department) # Get subjects associated with the teacher
    if selected_semester:
        teacher_subjects = teacher_subjects.filter(semester=selected_semester)

    # Initialize a list to hold the courses and their corresponding students
    courses_with_students = []
    
    for subject in teacher_subjects:
        # Get students associated with each course (subject)
        students_in_course = Student.objects.filter(subjects=subject).distinct()
        if selected_semester:
            students_in_course = students_in_course.filter(semester=selected_semester)
        
        # Append each course with its students to the list
        courses_with_students.append({
            'course': subject,
            'students': students_in_course
        })
   

    if request.method == 'POST':
        if 'multiple_choice_submit' in request.POST:
            multiple_choice_form = MultipleChoiceExamForm(request.POST)
            if multiple_choice_form.is_valid():
                exam = multiple_choice_form.save(commit=False) 
                exam.teacher = teacher
                multiple_choice_form.save()
                exam = multiple_choice_form.save()  # Save the form and get the exam
                return redirect('create_questions', exam_id=exam.id)
        elif 'subjective_submit' in request.POST:
            subjective_form = SubjectiveExamForm(request.POST)
            if subjective_form.is_valid():
                exam = subjective_form.save(commit=False)  # Create an exam instance but don't save yet
                exam.teacher = teacher
                subjective_form.save()
                exam = subjective_form.save()  # Save the form and get the exam
                return redirect('subjective_question', exam_id=exam.id)
        elif 'short_essay_submit' in request.POST:
            short_essay_form = ShortEssayExamForm(request.POST, teacher_subjects=teacher_subjects)
            if short_essay_form.is_valid():
                exam = short_essay_form.save(commit=False)
                exam.teacher = teacher
                exam.save()
                return redirect('teacher_dashboard')
    else:
        multiple_choice_form = MultipleChoiceExamForm()
        multiple_choice_form.fields['subject'].queryset = teacher_subjects 

        subjective_form = SubjectiveExamForm()
        subjective_form.fields['subject'].queryset = teacher_subjects 

        short_essay_form = ShortEssayExamForm(teacher_subjects=teacher_subjects)


    all_semesters = Subject.objects.filter(department=teacher.department).values_list('semester', flat=True).distinct().order_by('semester')
    exams = Exam.objects.filter(teacher=teacher)
    context = {
        'teacher_subjects': teacher_subjects,
        'total_courses': teacher_subjects.count(),  # Total courses (subjects)
        'courses_with_students': courses_with_students,  # Courses and their students
        'total_students': Student.objects.filter(subjects__in=teacher_subjects).distinct().count(),  # Total unique students
        'multiple_choice_form': multiple_choice_form,  # Pass the form instance
        'subjective_form': subjective_form,
        'short_essay_form': short_essay_form,
        # 'exam': exam
        'exams': exams,
        'selected_semester': selected_semester,
        'all_semesters': all_semesters,
        'semesters': SEMESTER_CHOICES,
    }

    # teacher = Teacher.objects.get(user=request.user)  # Get the Teacher associated with the logged-in user
     
    
    return render(request, 'teacher_dashboard.html', context)


def create_questions(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)  # Fetch the exam using the provided ID

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)  # Create question instance but don't save yet
            question.exam = exam  # Associate the question with the exam
            question.save()  # Now save the question
            return redirect('create_questions', exam_id=exam.id)  # Redirect to the same page to add more questions
    else:
        form = QuestionForm()

    context = {
        'exam': exam,
        'form': QuestionForm,
        
    }
    
    return render(request, 'create_questions.html', context)

def subjective_question(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)  # Fetch the exam using the provided ID

    if request.method == 'POST':
        subjective_form = SubjectiveQuestionForm(request.POST)
        if subjective_form.is_valid():
            question = subjective_form.save(commit=False)  # Create question instance but don't save yet
            question.exam = exam  # Associate the question with the exam
            question.save()  # Now save the question
            return redirect('subjective_question', exam_id=exam.id)  # Redirect to the same page to add more questions
    else:
        subjective_form = SubjectiveQuestionForm()

    context = {
        'subjective_form': SubjectiveQuestionForm,
        'exam': exam,
        
    }
    
    return render(request, 'subjective_question.html', context)


def edit_exam(request, id):
    # Retrieve the exam object or return a 404 error if not found
    exam = get_object_or_404(Exam, id=id)

    if request.method == 'POST':
        if exam.exam_type == 'MC':
            form = MultipleChoiceExamForm(request.POST, instance=exam)
            if form.is_valid():
                form.save()
                return redirect('teacher_dashboard')
        elif exam.exam_type == 'ST':
            form = SubjectiveExamForm(request.POST, instance=exam)
            if form.is_valid():
                form.save()
                return redirect('teacher_dashboard')
        elif exam.exam_type == 'SE':
            form = ShortEssayExamForm(request.POST, instance=exam)
            if form.is_valid():
                form.save()
                return redirect('teacher_dashboard')
    else:
        if exam.exam_type == 'MC':
            form = MultipleChoiceExamForm(instance=exam)
        elif exam.exam_type == 'ST':
            form = SubjectiveExamForm(instance=exam)
        elif exam.exam_type == 'SE':
            form = ShortEssayExamForm(instance=exam)

    context = {
        'exam': exam,
        'multiple_choice_form': form if exam.exam_type == 'MC' else None,
        'subjective_form': form if exam.exam_type == 'ST' else None,
        'short_essay_form': form if exam.exam_type == 'SE' else None,
    }
    return render(request, 'edit_exam.html', context)

    
def delete_exam(request, id):
    exam = get_object_or_404(Exam, id=id)
    exam.delete()  
    return redirect('teacher_dashboard')

@csrf_exempt
def toggle_publish(request, exam_id):
    if request.method == 'POST':
        try:
            exam = Exam.objects.get(id=exam_id)
            # Get the published status from the request body
            data = json.loads(request.body)
            exam.published = data.get('published', False)
            exam.save()
            return JsonResponse({'success': True})
        except Exam.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Exam not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def view_exam_questions(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    mcq_questions = Question.objects.filter(exam=exam).order_by('id')
    subjective_questions = SubjectiveQuestion.objects.filter(exam=exam).order_by('id')

    mcq_paginator = Paginator(mcq_questions, 1)
    subjective_paginator = Paginator(subjective_questions, 1) 
    mcq_page_number = request.GET.get('mcq_page')
    subjective_page_number = request.GET.get('subjective_page')

    mcq_page_obj = mcq_paginator.get_page(mcq_page_number)
    subjective_page_obj = subjective_paginator.get_page(subjective_page_number)

    context = {
        'exam': exam,
        'mcq_page_obj': mcq_page_obj,
        'subjective_page_obj': subjective_page_obj,
    }

    return render(request, 'view_questions.html', context)

def generate_pdf(request, exam_id):
    exam = Exam.objects.get(id=exam_id)
    questions = Question.objects.filter(exam=exam)
    template_path = 'pdf_MCQs.html'
    context = {'exam': exam, 'questions': questions}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{exam.exam_title}_questions.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error while generating PDF')
    return response

def unroll_course(request, id):
    student = Student.objects.get(user=request.user)
    subject = get_object_or_404(Subject, id=id)

    if subject in student.subjects.all():
        student.subjects.remove(subject)
        return redirect('student_dashboard')
    return JsonResponse({'status': 'failed'})


def enroll_course(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        print(f"Selected subject ID: {subject_id}")
        try:
            student = Student.objects.get(user=request.user)
            subject = Subject.objects.get(id=subject_id)
            student.subjects.add(subject)  # Enroll student in subject
            messages.success(request, f'You have successfully enrolled in {subject.name}.')
        except Subject.DoesNotExist:
            messages.error(request, 'Selected subject does not exist.')
        return redirect('student_dashboard')
    



def auto_save_exam(request, exam_id):
    if request.method == 'POST':
        exam = get_object_or_404(Exam, id=exam_id)
        answers = {}

        for key, value in request.POST.items():
            if key.startswith('question_'):
                question_id = key.split('_')[1]
                answers[int(question_id)] = value

        # Save answers to the database (you can create a temporary model or session-based storage)
        # Example: StudentAutoSave.objects.update_or_create(
        #     student=request.user, exam=exam, defaults={'answers': answers}
        # )

        return JsonResponse({'success': True, 'message': 'Answers auto-saved successfully!'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


def exam_results(request, exam_id):
    try:
        exam = Exam.objects.get(id=exam_id)
        # Use filter().first() instead of get() to avoid MultipleObjectsReturned
        student = Student.objects.get(user=request.user)
        student_exam = StudentExam.objects.filter(exam=exam, student=student).first()
        if not student_exam:
            return HttpResponse("Result not available", status=404)

        if student_exam.total_marks > 0:  # Prevent division by zero
            percentage = (student_exam.obtained_marks / student_exam.total_marks) * 100
        else:
            percentage = 0  # Default to 0% if no marks assigned

        context = {
            'exam': exam,
            'student_exam': student_exam,
            'percentage': round(percentage, 2),  # Round to 2 decimal places
        }
        return render(request, 'exam_results.html', context)

    except Exam.DoesNotExist:
        return HttpResponse("Exam not found", status=404)

def take_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    if exam.exam_type == "MC":
        questions = exam.questions.all()
    else:
        questions = exam.subjective_question.all()

    total_questions = questions.count()  # Count total questions
    question_time = total_questions * 60  # Set timer to 1 min per question

    context = {
        "exam": exam,
        "questions": questions, 
        "question_time": question_time,  # Dynamic timer
    }

    return render(request, "take_exam.html", context)

@login_required
def all_results(request):
    student = Student.objects.get(user=request.user)

    student_exams = StudentExam.objects.filter(student=student).order_by('-id')  # most recent first
    return render(request, 'result.html', {'student_exams': student_exams})

def submit_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    student = Student.objects.get(user=request.user)

    total_marks = 0
    obtained_marks = 0

    # Check if student already submitted
    existing_exam = StudentExam.objects.filter(exam=exam, student=student).first()
    if existing_exam:
        messages.success(request, "You have already submitted this exam. Viewing your result.")
        return redirect('exam_results', exam_id=exam.id)

    # 🛠 Corrected fetching questions based on exam type
    if exam.exam_type == "MC":
        questions = exam.questions.all()
    else:
        questions = exam.subjective_question.all()

    transformer = SentenceTransformer('all-MiniLM-L6-v2')

    if request.method == "POST":
        try:
            with transaction.atomic():
                for question in questions:
                    if exam.exam_type == "MC":
                        total_marks += question.marks
                        student_answer = request.POST.get(f'answer_{question.id}', '').strip()
                        if student_answer and int(student_answer) == int(question.correct_option):
                            obtained_marks += question.marks

                    else:  # Subjective or Short/Essay
                        total_marks += question.STmarks
                        student_answer = request.POST.get(f'answer_{question.id}', '').strip()
                        if student_answer:
                            reference_answer = question.reference_answer
                            embeddings = transformer.encode([reference_answer, student_answer])
                            similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]

                            awarded_marks = question.STmarks * similarity
                            obtained_marks += awarded_marks

                            # Save subjective answer
                            SubjectiveAnswer.objects.create(
                                question=question,
                                student=student,
                                student_answer=student_answer,
                                marks_awarded=awarded_marks
                            )

                # Save StudentExam
                student_exam = StudentExam.objects.create(
                    student=student,
                    exam=exam,
                    subject=exam.subject.name,
                    exam_title=exam.exam_title,
                    total_marks=total_marks,
                    obtained_marks=obtained_marks,
                    status='taken'
                )
                student_exam.save()

        except Exception as e:
            return HttpResponse(f"An error occurred: {e}")

    return redirect('exam_results', exam_id=exam.id)


@require_GET
def get_exam_analysis(request, exam_id):
    try:
        exam = Exam.objects.get(id=exam_id)
        questions = SubjectiveQuestion.objects.filter(exam=exam)
        student = Student.objects.get(user=request.user)
        answers = SubjectiveAnswer.objects.filter(student=student, question__in=questions)


        correct = 0
        incorrect = 0
        total_similarity = 0
        num_questions = questions.count()

        weak_topics = []
        detailed = []
        topic_counter = Counter()

        for q in questions:
            student_ans = answers.filter(question=q).first()
            student_text = student_ans.student_answer.strip() if student_ans else ""
            correct_text = q.reference_answer.strip()

            similarity = get_similarity(student_text, correct_text)
            total_similarity += similarity  # Accumulate total similarity

            marks_awarded = (similarity * q.STmarks)  # Calculate marks based on similarity percentage
            percentage = (marks_awarded / q.STmarks) * 100 

            is_correct = percentage >= 0.75
            topic = extract_topic_from_question(q.question_text)
            topic_counter[topic] += 1

            link = topic_links.get(topic, f"https://www.google.com/search?q={topic.replace(' ', '+')}")

            detailed.append({
                "question": q.question_text,
                "your_answer": student_text or "Not Answered",
                "correct_answer": correct_text,
                "status": f"Correct ({int(percentage)}%)" if is_correct else f"Incorrect ({int(percentage)}%)",
                "topic": topic,
                "external_link": link
            })

            if is_correct:
                correct += 1
            else:
                incorrect += 1
                weak_topics.append(topic)

        # Calculate average percentage-based correctness
        avg_correct = round((total_similarity / num_questions) * 100) if num_questions > 0 else 0
        avg_incorrect = 100 - avg_correct

        return JsonResponse({
            "exam": exam.exam_title,
            "correct": correct,        #Number Of Satisfied Answer 
            "incorrect": incorrect,    #Number Of Need to improve Answer
            "weak_topics": list(set(weak_topics)),
            "topics": topic_counter,
            "average_correct": avg_correct,
            "average_incorrect": avg_incorrect,
            "details": detailed
        })

    except Exam.DoesNotExist:
        return JsonResponse({'error': 'Exam not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    



@login_required
def student_profile_view(request):
    try:
        # Fetch the student object based on the logged-in user
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        # Handle the case where no student profile exists for the logged-in user
        messages.error(request, "Your profile does not exist.")
        return redirect('home')  # Redirect to a fallback page, like homepage or login page

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = StudentProfileForm(request.POST, request.FILES, instance=student)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('student_profile')  # Redirect back to the profile page
        else:
            # Handle form errors (if any)
            messages.error(request, "There was an error updating your profile. Please try again.")

    else:
        # Instantiate forms with current user and student data
        user_form = UserUpdateForm(instance=request.user)
        profile_form = StudentProfileForm(instance=student)

    return render(request, 'student_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })




def teacher_results_view(request):
    teacher = request.user.teacher
    exams = Exam.objects.filter(teacher=teacher).select_related('subject')

    enriched_exams = []
    for exam in exams:
        student_exams = StudentExam.objects.filter(exam=exam).select_related('student')
        total_students = student_exams.count()
        passed = student_exams.filter(obtained_marks__gte=exam.passing_marks).count()
        failed = total_students - passed
        avg_score = student_exams.aggregate(Avg('obtained_marks'))['obtained_marks__avg'] or 0

        enriched_student_exams = []
        for se in student_exams:
            answers = SubjectiveAnswer.objects.filter(student=se.student, question__exam=exam).select_related('question')
            analysis = [
                {
                    'question': a.question.question_text,
                    'answer': a.student_answer,
                    'marks': a.marks_awarded
                } for a in answers
            ]
            se.analysis = analysis
            enriched_student_exams.append(se)

        enriched_exams.append({
            'id': exam.id,
            'exam_title': exam.exam_title,
            'subject': exam.subject,
            'total_students': total_students,
            'passed': passed,
            'failed': failed,
            'avg_score': (avg_score / exam.total_marks * 100) if exam.total_marks else 0,
            'student_exams': enriched_student_exams
        })

    return render(request, 'teacher_results.html', {'exams': enriched_exams})
