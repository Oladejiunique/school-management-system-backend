from django.contrib import admin
from .models import ExamRecord, ReportCard


@admin.register(ExamRecord)
class ExamRecordAdmin(admin.ModelAdmin):
    list_display = ("student", "subject", "term", "score", "grade")
    list_filter = ("term", "subject", "grade")
    search_fields = ("student__username", "student__first_name", "student__last_name")


@admin.register(ReportCard)
class ReportCardAdmin(admin.ModelAdmin):
    list_display = ("student", "term", "school_class", "created_at")
    list_filter = ("term", "school_class")
    search_fields = ("student__username", "student__first_name", "student__last_name")
