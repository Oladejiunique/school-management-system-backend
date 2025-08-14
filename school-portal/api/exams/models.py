from django.conf import settings
from django.db import models
from django.utils import timezone

class Exam(models.Model):
    name = models.CharField(max_length=128)
    term = models.ForeignKey("academics.Term", on_delete=models.SET_NULL, null=True, blank=True)
    school_class = models.ForeignKey("academics.SchoolClass", on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = ("name", "school_class", "term")

    def __str__(self):
        return f"{self.name} - {self.school_class}"


class Assessment(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.ForeignKey("academics.Subject", on_delete=models.SET_NULL, null=True, blank=True)
    marks_obtained = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    max_marks = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    grade = models.CharField(max_length=8, blank=True)

    class Meta:
        unique_together = ("exam", "student", "subject")

    def __str__(self):
        return f"{self.student} - {self.exam} - {self.subject}"


from django.conf import settings
from django.db import models
from academics.models import Term, Subject, SchoolClass


class ExamRecord(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="exam_records")
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name="exam_records")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="exam_records")
    score = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=2, blank=True)  # e.g., A, B, C
    remarks = models.TextField(blank=True)

    class Meta:
        unique_together = ("student", "term", "subject")

    def __str__(self):
        return f"{self.student} - {self.subject} ({self.score})"


class ReportCard(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="report_cards")
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name="report_cards")
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name="report_cards")
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "term", "school_class")

    def __str__(self):
        return f"Report Card: {self.student} - {self.term}"

