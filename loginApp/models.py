from django.db import models
from django.contrib.auth.models import User
import random

class CustomerSignUp(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, null=True)  
    last_name = models.CharField(max_length=100, blank=True, null=True)   
    email = models.EmailField(unique=True)  # Ensure uniqueness
    phone = models.CharField(max_length=15, default="0000000000", blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True, default="Customer")
    information = models.TextField(blank=True, null=True)

    otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def generate_otp(self):
        """Generates a 6-digit OTP, saves it in the database, and returns it."""
        self.otp = str(random.randint(100000, 999999))
        self.save()
        return self.otp



class LoanRequest(models.Model):
    customer = models.ForeignKey(CustomerSignUp, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tenure = models.IntegerField()  # Number of months
    interest_rate = models.FloatField()
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
        default='pending'
    )

    def __str__(self):
        return f"Loan Request by {self.customer.user.username} - {self.amount}"
    






# class CustomerLogin(models.Model):
#     username = models.CharField(max_length=250, blank=False, null=False)
#     password = models.PasswordField(max_length=100, blank=False)

# Create your models here.






# class CustomerLogin(models.Model):
#     username = models.CharField(max_length=250, blank=False, null=False)
#     password = models.PasswordField(max_length=100, blank=False)

# Create your models here.
