from rest_framework import serializers
from .models import ExamRecord, ReportCard
from users.serializers import UserSerializer
from academics.serializers import TermSerializer, SubjectSerializer, SchoolClassSerializer


class ExamRecordSerializer(serializers.ModelSerializer):
    student = UserSerializer()
    term = TermSerializer()
    subject = SubjectSerializer()

    class Meta:
        model = ExamRecord
        fields = "__all__"


class ReportCardSerializer(serializers.ModelSerializer):
    student = UserSerializer()
    term = TermSerializer()
    school_class = SchoolClassSerializer()

    class Meta:
        model = ReportCard
        fields = "__all__"
