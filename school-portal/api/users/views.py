from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.encoding import smart_bytes, smart_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from rest_framework import viewsets, status, generics, permissions
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from django_filters.rest_framework import DjangoFilterBackend
from django.http import StreamingHttpResponse
import csv

from .models import User, StudentProfile
from .serializers import UserSerializer, StudentProfileSerializer
from .permissions import IsAdmin, IsTeacherOrAdmin, IsOwnerOrAdmin


# -------------------------------
# Password Reset Flow
# -------------------------------

class RequestPasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email_or_reg_no = request.data.get("email") or request.data.get("email_or_reg_no")
        if not email_or_reg_no:
            return Response({"error": "Email or registration number is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email_or_reg_no).first() or \
               User.objects.filter(user_id=email_or_reg_no).first()

        reset_link = None
        if user:
            token = PasswordResetTokenGenerator().make_token(user)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            reset_link = f"{settings.FRONTEND_URL}/reset-password?uid={uidb64}&token={token}"
        else:
            # Fake link to avoid revealing that user doesn't exist
            reset_link = f"{settings.FRONTEND_URL}/reset-password?uid=fake&token=fake"

        try:
            send_mail(
                subject="Password Reset Request",
                message="If you requested a password reset for your account with our School Management System, "
                f"please click the link below to proceed:\n{reset_link}\n\n"
                "If you did not make this request, please ignore this message or contact our support team immediately.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email_or_reg_no],
                fail_silently=False,
            )
            print(f"[DEBUG] Email sent to {email_or_reg_no}")
        except Exception as e:
            print(f"[ERROR] Email sending failed: {e}")

        return Response({"success": "If the account exists, a reset link has been sent."}, status=status.HTTP_200_OK)


class ValidateResetTokenView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """
        GET /auth/password-reset-validate/?uid=<uid>&token=<token>
        """
        uidb64 = request.query_params.get("uid")
        token = request.query_params.get("token")
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
        except Exception:
            return Response({"valid": False}, status=status.HTTP_200_OK)

        valid = PasswordResetTokenGenerator().check_token(user, token)
        return Response({"valid": bool(valid)}, status=status.HTTP_200_OK)


class ResetPasswordConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        POST { "uid": "...", "token": "...", "password": "newStrongPassword123" }
        On success:
          - sets new password
          - issues SimpleJWT tokens (auto-login)
        """
        uidb64 = request.data.get("uid")
        token = request.data.get("token")
        password = request.data.get("password")

        if not all([uidb64, token, password]):
            return Response({"error": "uid, token, and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            return Response({"error": "Invalid user"}, status=status.HTTP_400_BAD_REQUEST)

        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        user_payload = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }

        return Response(
            {
                "success": "Password has been reset successfully",
                "access": str(access),
                "refresh": str(refresh),
                "user": user_payload,
            },
            status=status.HTTP_200_OK,
        )


# -------------------------------
# User & Student Management
# -------------------------------

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ("username", "first_name", "last_name", "email")
    ordering_fields = ("username", "email")


class StudentViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all().order_by("user__first_name", "user__last_name")
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = (
        "user__first_name",
        "user__last_name",
        "school_class__name",
        "guardian_name",
        "guardian_phone",
        "user__email",
    )
    ordering_fields = (
        "user__first_name",
        "user__last_name",
        "school_class__name",
        "guardian_name",
        "user__email",
    )

    def get_permissions(self):
        if self.action in ("create", "destroy"):
            permission_classes = [IsAuthenticated, IsAdmin]
        elif self.action in ("update", "partial_update"):
            permission_classes = [IsAuthenticated, (IsTeacherOrAdmin | IsOwnerOrAdmin)]
        else:
            permission_classes = [IsAuthenticated]
        return [p() for p in permission_classes]

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated, IsAdmin])
    def export_csv(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        def stream():
            header = ["id", "name", "class", "age", "guardian", "email"]
            writer = csv.writer(Echo())
            yield writer.writerow(header)
            for s in queryset.iterator():
                age = ""
                if s.user.date_of_birth:
                    today = timezone.now().date()
                    age = today.year - s.user.date_of_birth.year - (
                        (today.month, today.day) < (s.user.date_of_birth.month, s.user.date_of_birth.day)
                    )
                yield writer.writerow([
                    s.id,
                    s.user.get_full_name(),
                    s.school_class.name if s.school_class else "",
                    age,
                    s.guardian_name,
                    s.user.email or ""
                ])

        return StreamingHttpResponse(stream(), content_type="text/csv")


class Echo:
    def write(self, value):
        return value
