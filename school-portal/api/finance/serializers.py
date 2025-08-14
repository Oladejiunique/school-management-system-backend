from rest_framework import serializers
from .models import FeeType, Invoice, Payment
from users.serializers import UserSerializer


class FeeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeType
        fields = "__all__"


class InvoiceSerializer(serializers.ModelSerializer):
    student = UserSerializer()
    fee_type = FeeTypeSerializer()

    class Meta:
        model = Invoice
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    invoice = InvoiceSerializer()

    class Meta:
        model = Payment
        fields = "__all__"
