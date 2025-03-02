from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from django.db import IntegrityError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .forms import CustomerSignUpForm, CustomerLoginForm, UpdateCustomerForm
from .models import CustomerSignUp
from .utils import send_otp_email 


# 🔹 Home View
def home_view(request):
    return render(request, 'home.html')


# 🔹 User Registration API (Handles errors properly)
class RegisterUser(APIView):
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not username or not email or not password:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email is already registered"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"error": "A database error occurred. Please try again."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 🔹 JWT Login API (Improved authentication)
@api_view(['POST'])
def login_user(request):
    """Authenticate user and return JWT tokens only if verified."""
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        customer = CustomerSignUp.objects.get(user=user)
        if not customer.is_verified:
            return Response({'error': 'Account not verified. Please verify your OTP.'}, status=status.HTTP_403_FORBIDDEN)
    except CustomerSignUp.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    # ✅ Generate JWT Tokens
    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'username': user.username
    })


# 🔹 Customer Sign Up (Form-based, prevents duplicate email)
def sign_up_view(request):
    """Handles customer registration and sends OTP for email verification."""
    if request.user.is_authenticated:
        return redirect('loginApp:home')

    form = CustomerSignUpForm()
    error = ""

    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            if User.objects.filter(email=email).exists():
                error = "Email is already in use. Please log in."
            elif User.objects.filter(username=username).exists():
                error = "Username already exists. Try a different one."
            else:
                # ✅ Create user
                user = form.save(commit=False)
                user.save()

                # ✅ Create customer profile & generate OTP
                customer = CustomerSignUp.objects.create(user=user, email=email)
                otp = customer.generate_otp()
                send_otp_email(customer.email, otp)

                return redirect('loginApp:verify_otp', user_id=customer.id)

    return render(request, 'loginApp/signup.html', {'form': form, 'error': error})


# 🔹 Logout (Prevents accidental logouts)
@login_required(login_url='/account/login-customer')
def logout_view(request):
    """Logs out the user and redirects to the login page."""
    if request.method == "POST":  # Prevent accidental logouts via GET
        logout(request)
        return redirect('loginApp:login_customer')  
    return render(request, 'loginApp/logout.html')  # Render logout confirmation page


# 🔹 Protected API View (✅ Requires JWT Authentication)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    """Example of an API that requires JWT authentication"""
    return Response({"message": f"Hello {request.user.username}, you are authenticated!"})


# 🔹 OTP Verification (Handles incorrect OTP attempts)
def verify_otp(request, user_id):
    """Verify OTP and activate user account."""
    try:
        customer = CustomerSignUp.objects.get(id=user_id)
    except CustomerSignUp.DoesNotExist:
        messages.error(request, "Invalid user.")
        return redirect('loginApp:signup')

    if request.method == "POST":
        entered_otp = request.POST.get("otp")

        if customer.otp == entered_otp:
            customer.is_verified = True
            customer.otp = None  # Clear OTP after verification
            customer.save()

            messages.success(request, "OTP verified successfully! You can now log in.")
            return redirect('loginApp:login_customer')  # Redirect to login page
        else:
            messages.error(request, "Invalid OTP. Try again.")

    return render(request, 'loginApp/verify_otp.html', {'customer': customer})


# 🔹 Edit Customer Profile (Handles form validation properly)
@login_required(login_url='/account/login-customer')
def edit_customer(request):
    """Allow users to edit their profile."""
    customer = request.user.customersignup  # Assuming OneToOne relation with User
    form = UpdateCustomerForm(instance=customer)

    if request.method == 'POST':
        form = UpdateCustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('edit_customer')

    return render(request, 'loginApp/edit_customer.html', {'form': form})















# Create your views here.
