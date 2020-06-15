from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import Profile, User, Vendor


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address.')
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'address', 'phone_number','password1', 'password2']
    def save(self, commit=True):
        user = super().save(commit=commit)
        user.is_vendor = False
        if commit:
            user.save()
        return user

class VendorRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address.')
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'address', 'phone_number','password1', 'password2']
    def save(self, commit=True):
        user = super().save(commit=commit)
        user.is_vendor = True
        if commit:
            user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'address', 'phone_number']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class LoginForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password']

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        if not authenticate(email=email, password=password):
            raise forms.ValidationError("Invalid Login")
    
class VendorUpdateForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = [
            'company_name', 'legal_name', 'address', 'business_type' ,'contact_name', 'phone_number', 'website',
            'banner',
            'business_structure', 'length_of_operation', 'number_of_employees', 'location_type', 'special_business',
        ]

class AdminVendorUpdateForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = [
            'bank_name', 'branch_location', 'aba_number', 'account_number',
            'tax_credits', 'rate',
            'approved'
        ]