from rest_framework import serializers
from .models import User, StudentProfile, TeacherProfile, ParentProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "username", "first_name", "middle_name", "last_name",
            "email", "photo", "role", "user_id", "phone", "bio",
            "gender", "date_of_birth", "address"
        ]


class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = StudentProfile
        fields = ["id", "user", "school_class", "guardian_name", "guardian_phone", "created_at", "updated_at"]


class TeacherProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    subjects = serializers.StringRelatedField(many=True)

    class Meta:
        model = TeacherProfile
        fields = ["id", "user", "subjects", "created_at", "updated_at"]


class ParentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    children = UserSerializer(many=True)

    class Meta:
        model = ParentProfile
        fields = ["id", "user", "children", "created_at", "updated_at"]
