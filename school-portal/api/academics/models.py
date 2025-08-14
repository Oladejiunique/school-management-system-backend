from django.conf import settings
from django.db import models


class AcademicYear(models.Model):
    name = models.CharField(max_length=50, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Term(models.Model):
    name = models.CharField(max_length=50)  # e.g., "First Term"
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name="terms")
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    class Meta:
        unique_together = ("name", "academic_year")

    def __str__(self):
        return f"{self.name} - {self.academic_year}"


class SchoolClass(models.Model):
    name = models.CharField(max_length=50)  # e.g., "JSS1"
    grade_level = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=50)  # e.g., "A"
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name="sections")

    class Meta:
        unique_together = ("name", "school_class")

    def __str__(self):
        return f"{self.school_class} - {self.name}"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, blank=True, null=True)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name="subjects")

    def __str__(self):
        return self.name


class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="assignments")
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Exam(models.Model):
    name = models.CharField(max_length=255)
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name="exams")
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name="exams")
    exam_date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.term})"


class Assessment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assessments")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="assessments")
    score = models.DecimalField(max_digits=5, decimal_places=2)
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name="assessments")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "subject", "term")

    def __str__(self):
        return f"{self.student} - {self.subject} ({self.score})"


class Attendance(models.Model):
    STATUS_PRESENT = "present"
    STATUS_ABSENT = "absent"
    STATUS_LATE = "late"

    STATUS_CHOICES = [
        (STATUS_PRESENT, "Present"),
        (STATUS_ABSENT, "Absent"),
        (STATUS_LATE, "Late"),
    ]

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="attendances")
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PRESENT)
    remarks = models.TextField(blank=True)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.SET_NULL, null=True, blank=True)
    term = models.ForeignKey(Term, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ("student", "date")

    def __str__(self):
        return f"{self.student} - {self.date} ({self.status})"
