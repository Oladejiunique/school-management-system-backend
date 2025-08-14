from django.contrib import admin
from .models import FeeType, Invoice, Payment


@admin.register(FeeType)
class FeeTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "amount")
    search_fields = ("name",)


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("student", "fee_type", "amount", "due_date", "status", "issued_at")
    list_filter = ("status", "fee_type", "due_date")
    search_fields = ("student__username", "student__first_name", "student__last_name")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("invoice", "amount_paid", "payment_date", "method")
    list_filter = ("method", "payment_date")
    search_fields = ("invoice__student__username", "invoice__student__first_name", "invoice__student__last_name")
