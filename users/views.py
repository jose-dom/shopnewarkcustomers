from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, VendorRegisterForm, LoginForm, VendorUpdateForm, AdminVendorUpdateForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import User, Vendor
from core.models import Trans
import boto3
import uuid


def error_view(request):
    if request.user.is_authenticated:
        messages.warning(request,f'Invalid Request. Please report any issue to via email to developer@jasfel.com')
        return redirect('profile')
    else:
        messages.warning(request,f'Invalid Request. Please Login.')
        return redirect('login')

def error_view_400(request, exception):
    if request.user.is_authenticated:
        messages.warning(request,f'Invalid Request. Please report any issue to via email to developer@jasfel.com')
        return redirect('profile')
    else:
        messages.warning(request,f'Invalid Request. Please Login.')
        return redirect('login')

def register_cus(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'You have successfully registered!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register_cus.html', {'form': form})

def register_ven(request):
    if request.method == 'POST':
        form = VendorRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'You have successfully registered! Continue with providing more information on your company/organization.')
            email = request.POST['email']
            password = request.POST['password1']
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('vendor-create')
    else:
        form = VendorRegisterForm()
    return render(request, 'users/register_ven.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, 'users/logout.html')

def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('dashboard')

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user and user.is_vendor == False:
                login(request, user)
                return redirect('profile')
            elif user and user.is_vendor == True and user.vendor:
                login(request, user)
                return redirect('profile')
            else:
                messages.warning(request, f'You may not be registered!')
    else:
        form = LoginForm()
    context['form'] = form

    return render(request, "users/login.html", context)

@login_required
def profile(request):
    return render(request, 'users/profile.html')

@login_required
def profile_update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/profile_update.html', context)

def vendor_transactions(request):
    transactions = Trans.objects.all().filter(vendor=request.user.vendor)
    total_amount = 0 
    for t in transactions:
        if t.sale_type == "Sale":
            total_amount += t.amount
        elif t.sale_type == "1":
            total_amount += t.amount
        elif t.sale_type == "Return":
            total_amount -= t.amount
        elif t.sale_type == "Other":
            total_amount += t.amount
    context = {
        'trans': transactions,
        'total_amount': round(total_amount,2)
    }
    return render(request, 'users/trans_ven.html', context)

def customer_transactions(request):
    transactions = Trans.objects.all().filter(customer=request.user)
    total_amount = 0 
    for t in transactions:
        if t.sale_type == "Sale":
            total_amount += t.amount
        elif t.sale_type == "1":
            total_amount += t.amount
        elif t.sale_type == "Return":
            total_amount -= t.amount
        elif t.sale_type == "Other":
            total_amount += t.amount
    context = {
        'trans': transactions,
        'total_amount': round(total_amount,2)
    }
    return render(request, 'users/trans_cus.html', context)

class VendorCreateView(LoginRequiredMixin, CreateView):
    model = Vendor
    fields = ['company_name', 'legal_name', 'address', 'business_type' ,'contact_name', 'phone_number', 'website',
            'bank_name', 'branch_location', 'aba_number', 'account_number',
            'banner',
            'business_structure', 'length_of_operation', 'number_of_employees', 'location_type', 'special_business',
            'tax_credits', 'rate',
            'terms_conditions'
    ]

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class VendorDetailView(DetailView):
    model = Vendor

class VendorUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Vendor

    fields = [
            'company_name', 'legal_name', 'address', 'business_type' ,'contact_name', 'phone_number', 'website',
            'bank_name', 'branch_location', 'aba_number', 'account_number',
            'banner',
            'business_structure', 'length_of_operation', 'number_of_employees', 'location_type', 'special_business',
            'tax_credits', 'rate',
            'terms_conditions'
    ]

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        vendor = self.get_object()
        if self.request.user == vendor.owner:
            return True
        return False

def admin_dashboard(request):
    vendors = Vendor.objects.all()
    context = {
        'vendors': vendors,
    }
    return render(request, 'users/admin_dashboard.html', context)

def vendor_update(request):
    if request.method == 'POST':
        form = VendorUpdateForm(request.POST, instance=request.user.vendor)
        
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        form = VendorUpdateForm(instance=request.user.vendor)
    context = {
        'form': form,
    }
    return render(request, 'users/vendor_update.html', context)

def admin_vendor_update(request, ven_id):
    vendor = Vendor.objects.all().filter(pk=ven_id)[0]
    if request.method == 'POST':
        form = AdminVendorUpdateForm(request.POST, instance=vendor)
        
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('admin-dashboard')
    else:
        form = AdminVendorUpdateForm(instance=vendor)
    context = {
        'form': form,
        'ven_id': ven_id,
    }
    return render(request, 'users/vendor_update.html', context)
