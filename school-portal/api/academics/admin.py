from django.contrib import admin
from .models import AcademicYear, Term, SchoolClass, Section, Subject, Assignment, Exam, Assessment, Attendance


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ("name", "academic_year", "start_date", "end_date", "is_current")
    list_filter = ("academic_year", "is_current")
    search_fields = ("name", "academic_year__name")


@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ("name", "grade_level")
    list_filter = ("grade_level",)
    search_fields = ("name",)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("name", "school_class")
    list_filter = ("school_class",)
    search_fields = ("name", "school_class__name")


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "school_class")
    list_filter = ("school_class",)
    search_fields = ("name", "code")


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("title", "subject", "due_date", "created_at")
    list_filter = ("subject", "due_date")
    search_fields = ("title", "subject__name")


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ("name", "term", "school_class", "exam_date")
    list_filter = ("term", "school_class")
    search_fields = ("name", "term__name", "school_class__name")


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ("student", "subject", "score", "term", "created_at")
    list_filter = ("term", "subject")
    search_fields = ("student__username", "student__first_name", "student__last_name", "subject__name")


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("student", "date", "status", "school_class", "term")
    list_filter = ("status", "school_class", "term")
    search_fields = ("student__username", "student__first_name", "student__last_name")
