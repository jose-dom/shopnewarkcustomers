from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import SearchCustomerForm, AddTransactionForm, SearchCustomerEmailForm
from users.models import User
from .models import Trans
import uuid
import datetime

def home(request):
    return redirect('profile')

def search_customer(request):
    if request.method == 'POST':
        form = SearchCustomerForm(request.POST)
        
        if form.is_valid():
            phone_number = request.POST['phone_number']
            users = User.objects.all().filter(phone_number=phone_number)
            if users.count() == 0:
                messages.warning(request, f'No customers were found by that phone number. Perhaps try searching by email.')
                return redirect('search-customer')
            else:
                for u in users:
                    if u.is_vendor == False:
                        request.session['phone_number'] = phone_number
                        return redirect('customer-results')
                    else:
                        messages.warning(request, f'No customers were found by that phone number. Perhaps try searching by email.')
                        return redirect('search-customer')

    else:
        form = SearchCustomerForm()
    context = {
        'form': form,
    }
    return render(request, 'core/search_customer.html', context)

def search_customer_email(request):
    if request.method == 'POST':
        form = SearchCustomerEmailForm(request.POST)
        
        email = request.POST['email']
        users = User.objects.all().filter(email=email)
        if users.count() == 0:
            messages.warning(request, f'No customers were found by that email. Perhaps try searching by phone number.')
            return redirect('search-customer')
        else:
            for u in users:
                if u.is_vendor == False:
                    request.session['email'] = email
                    return redirect('customer-results-email')
                else:
                    messages.warning(request, f'No customers were found by that email. Perhaps try searching by phone number.')
                    return redirect('search-customer-email')
    else:
        form = SearchCustomerEmailForm()
    context = {
        'form': form,
    }
    return render(request, 'core/search_customer.html', context)

def customer_results(request):
    phone_number = request.session['phone_number']
    request.session['phone_number'] = phone_number
    users = User.objects.all().filter(phone_number=phone_number)
    if 'user' in request.POST:
        user_id = request.POST['user']
        request.session['user_id'] = user_id
        return redirect('transactions')

    context = {
        'phone_number': phone_number,
        'users': users
    }
    return render(request, 'core/customer_results.html', context)

def customer_results_email(request):
    email = request.session['email']
    request.session['email'] = email
    users = User.objects.all().filter(email=email)
    if 'user' in request.POST:
        user_id = request.POST['user']
        request.session['user_id'] = user_id
        return redirect('transactions')

    context = {
        'email': email,
        'users': users
    }
    return render(request, 'core/customer_results.html', context)

def transactions(request):
    user_id = request.session['user_id']
    cus = User.objects.all().filter(id=user_id)[0]
    if request.method == 'POST':
        form = AddTransactionForm(request.POST)
        if form.is_valid():
            vendor = request.user.vendor
            customer = cus
            trans = Trans(trans_id=str(uuid.uuid1()), customer=cus, vendor=vendor, amount=request.POST['amount'], sale_type=request.POST['sale_type'])
            trans.save()
            messages.success(request, f'Transaction was successfully entered. Search for another customer to enter a new transaction.')
            return redirect('search-customer')
    else:
        form = AddTransactionForm()
    context = {
        'user_id': user_id,
        'cus': cus,
        'form': form
    }
    return render(request, 'core/transactions.html', context)

'''
class TransCreateView(LoginRequiredMixin, CreateView):
    model = Trans
    fields = ['amount','sale_type']

    def form_valid(self, form):
        form.instance.customer = self.request.user
        return super().form_valid(form)
'''