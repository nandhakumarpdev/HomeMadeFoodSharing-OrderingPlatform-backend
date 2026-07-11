from django.core.mail import send_mail
from django.conf import settings

def send_otp_email(email, otp):
    send_mail(
        subject="Password Reset OTP",
        message=f"Your OTP is {otp}. It is valid for 5 minutes",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )