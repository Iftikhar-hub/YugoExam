# from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .admin import custom_admin_site
from . import views
urlpatterns = [
    path('admin/', custom_admin_site.urls),
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('about/', views.about, name='about'),
    path('teacher_login/', views.teacher_login, name='teacher_login'),
    path('teacher_register/', views.teacher_register, name='teacher_register'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('update_subjects/', views.update_subjects, name='update_subjects'),
    path('add_department/', views.add_department, name='add_department'),
    path('student/register/', views.student_register, name='student_register'),
    path('student_login/', views.student_login, name='student_login'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    
    path('create-questions/<int:exam_id>/', views.create_questions, name='create_questions'),
    path('subjective_question/<int:exam_id>/', views.subjective_question, name='subjective_question'),

    path('edit-exam/<int:id>/', views.edit_exam, name='edit_exam'),
    path('delete_exam/<int:id>/',views.delete_exam, name='delete_exam'),

    path('view-questions/<int:exam_id>/', views.view_exam_questions, name='view_exam_questions'),

    path('generate-pdf/<int:exam_id>/', views.generate_pdf, name='generate_pdf'),
    path('toggle-publish/<int:exam_id>/', views.toggle_publish, name='toggle_publish'),
    path('unroll_course/<int:id>/', views.unroll_course, name='unroll_course'),
    path('enroll_course/', views.enroll_course, name='enroll_course'),
    path('take-exam/<int:exam_id>/', views.take_exam, name='take_exam'),
    path('auto-save-exam/<int:exam_id>/', views.auto_save_exam, name='auto_save_exam'),
    path('submit-exam/<int:exam_id>/', views.submit_exam, name='submit_exam'),
    path('exam_results/<int:exam_id>/', views.exam_results, name='exam_results'),
    path('results/', views.all_results, name='all_results'),

    path('exam/analysis/<int:exam_id>/', views.get_exam_analysis, name='get_exam_analysis'),

    path('update_subjects/', views.update_subjects, name='update_subjects'),
    path('get_subjects/', views.get_subjects_by_department, name='get_subjects'),
    path('profile/', views.student_profile_view, name='student_profile'),
    path('teacher-results/', views.teacher_results_view, name='teacher_results'),

  





  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)