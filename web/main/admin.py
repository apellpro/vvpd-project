from django.contrib import admin
from .models import YearGroup, Student, Project

# Register your models here.

admin.site.register(YearGroup)
admin.site.register(Student)
admin.site.register(Project)