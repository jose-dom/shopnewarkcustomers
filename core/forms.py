from django import forms
from users.models import User
from .models import Trans

class SearchCustomerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['phone_number']

class SearchCustomerEmailForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['email']

class AddTransactionForm(forms.ModelForm):
    class Meta:
        model = Trans
        fields = ['amount', 'sale_type']