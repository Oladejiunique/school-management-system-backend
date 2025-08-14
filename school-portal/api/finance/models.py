from django.conf import settings
from django.db import models


class FeeType(models.Model):
    name = models.CharField(max_length=100, unique=True)  # e.g., Tuition, Library, Sports
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Invoice(models.Model):
    STATUS_PENDING = "pending"
    STATUS_PAID = "paid"
    STATUS_OVERDUE = "overdue"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_PAID, "Paid"),
        (STATUS_OVERDUE, "Overdue"),
    ]

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="invoices")
    fee_type = models.ForeignKey(FeeType, on_delete=models.CASCADE, related_name="invoices")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice: {self.student} - {self.fee_type} ({self.status})"


class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="payments")
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=50, blank=True)  # e.g., Bank Transfer, Cash

    def __str__(self):
        return f"Payment for {self.invoice} - {self.amount_paid}"
