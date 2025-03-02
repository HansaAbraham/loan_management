from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from loanApp.models import LoanCategory


class LoanCategoryForm(forms.ModelForm):
    class Meta:
        model = LoanCategory
        fields = ('loan_name',)


class AdminLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')