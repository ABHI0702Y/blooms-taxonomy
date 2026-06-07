from django.contrib import admin
from .models import College, Branch, Subject, Subject_data


@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'branch_count')
    search_fields = ('name', 'location')

    def branch_count(self, obj):
        return obj.branches.count()
    branch_count.short_description = 'Branches'


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'college', 'subject_count')
    list_filter = ('college',)
    search_fields = ('name', 'college__name')

    def subject_count(self, obj):
        return obj.subjects.count()
    subject_count.short_description = 'Subjects'


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject_code', 'branch', 'semester')
    list_filter = ('semester', 'branch__college')
    search_fields = ('name', 'subject_code', 'branch__name')


@admin.register(Subject_data)
class SubjectDataAdmin(admin.ModelAdmin):
    list_display = ('subject_name', 'branch_name', 'semester', 'faculty', 'exam_type', 'date', 'created_at')
    list_filter = ('semester', 'exam_type', 'branch_name')
    search_fields = ('subject_name', 'faculty', 'college_name')
    readonly_fields = ('created_at',)
