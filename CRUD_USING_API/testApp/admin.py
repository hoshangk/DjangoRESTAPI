from django.contrib import admin
from testApp.models import Student

# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id','name','rollno','marks','gf','bf']

admin.site.register(Student, StudentAdmin)