from django.contrib.admin import AdminSite
from django.contrib import admin
from django.http import HttpResponseForbidden
from .models import Department, Subject, Teacher, Student

# ✅ Custom AdminSite to restrict access to only staff users
class CustomAdminSite(AdminSite):
    def has_permission(self, request):
        return request.user.is_active and request.user.is_staff  # Only allow Django's default admin users

# ✅ Instantiate and name your custom site
custom_admin_site = CustomAdminSite(name='custom_admin')

# ✅ Admin model configurations
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'semester')
    list_filter = ('department', 'semester')
    search_fields = ('name',)

class TeacherAdmin(admin.ModelAdmin):
    def email(self, obj):
        return obj.user.email  # Assuming you have a OneToOneField with User in your Teacher model
    email.short_description = 'Email'
    list_display = ('first_name', 'last_name', 'email', 'department')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('department', 'subjects')

class StudentAdmin(admin.ModelAdmin):
    def email(self, obj):
        return obj.user.email  # Assuming you have a OneToOneField with User in your Student model
    email.short_description = 'Email'
    list_display = ('first_name', 'last_name', 'email', 'department',  'semester')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('department', 'subjects')

# ✅ Register models with the custom site
custom_admin_site.register(Department, DepartmentAdmin)
custom_admin_site.register(Subject, SubjectAdmin)
custom_admin_site.register(Teacher, TeacherAdmin)
custom_admin_site.register(Student, StudentAdmin)
