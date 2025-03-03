# utils.py - Function to send OTP email
from django.core.mail import send_mail
from django.conf import settings
import random

def send_otp_email(email, otp):
    subject = "Your OTP Code for Loan Management"
    message = f"Hello,\n\nYour One-Time Password (OTP) is: {otp}\n\nUse this code to verify your email.\n\nThank you!"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    import random

def generate_otp():
    return str(random.randint(100000, 999999))


    send_mail(subject, message, email_from, recipient_list)