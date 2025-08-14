from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, StudentProfile, TeacherProfile, ParentProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Additional Info", {
            "fields": (
                "middle_name", "photo", "role", "user_id",
                "phone", "bio", "gender", "date_of_birth", "address",
            ),
        }),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {
            "fields": (
                "middle_name", "photo", "role", "user_id",
                "phone", "bio", "gender", "date_of_birth", "address",
            ),
        }),
    )

    list_display = ("username", "first_name", "last_name", "middle_name", "role", "user_id", "email", "is_active")
    list_filter = ("role", "is_active", "is_staff", "is_superuser")
    search_fields = ("username", "first_name", "last_name", "middle_name", "email", "user_id", "phone")
    ordering = ("username",)


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "school_class", "guardian_name", "guardian_phone", "created_at")
    list_filter = ("school_class",)
    search_fields = ("user__username", "user__first_name", "user__last_name", "guardian_name", "guardian_phone")


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")
    filter_horizontal = ("subjects",)
    search_fields = ("user__username", "user__first_name", "user__last_name")


@admin.register(ParentProfile)
class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")
    filter_horizontal = ("children",)
    search_fields = ("user__username", "user__first_name", "user__last_name", "children__username")
