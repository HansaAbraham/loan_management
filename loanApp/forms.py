from django import forms
from .models import LoanRequest, LoanTransaction


class LoanRequestForm(forms.ModelForm):
    class Meta:
        model = LoanRequest
        fields = ('category', 'reason', 'amount', 'year')


class LoanTransactionForm(forms.ModelForm):
    class Meta:
        model = LoanTransaction
        fields = ('payment',)




# Create your views here.
