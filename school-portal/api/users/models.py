from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    ROLE_ADMIN = "admin"
    ROLE_TEACHER = "teacher"
    ROLE_STUDENT = "student"
    ROLE_PARENT = "parent"

    ROLE_CHOICES = (
        (ROLE_ADMIN, "Admin"),
        (ROLE_TEACHER, "Teacher"),
        (ROLE_STUDENT, "Student"),
        (ROLE_PARENT, "Parent"),
    )

    middle_name = models.CharField(max_length=120, blank=True, null=True)
    photo = models.ImageField(upload_to="users/photos/%Y/%m/", blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_STUDENT)
    user_id = models.CharField(max_length=50, blank=True, null=True, unique=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=16, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)

    class Meta:
        ordering = ("username",)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.role})"


class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_profile")
    school_class = models.ForeignKey("academics.SchoolClass", on_delete=models.SET_NULL, null=True, blank=True)
    guardian_name = models.CharField(max_length=255, blank=True)
    guardian_phone = models.CharField(max_length=32, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Student: {self.user.get_full_name()} - {self.school_class or 'No Class'}"


class TeacherProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="teacher_profile")
    subjects = models.ManyToManyField("academics.Subject", blank=True, related_name="teachers")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Teacher: {self.user.get_full_name()}"


class ParentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="parent_profile")
    children = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="parent_of")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Parent: {self.user.get_full_name()}"
