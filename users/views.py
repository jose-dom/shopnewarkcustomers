from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import User
import boto3
import uuid

dynamodb = boto3.resource("dynamodb")
dynamoTable = dynamodb.Table("Users")
dynamoTable_trans = dynamodb.Table("Transactions")

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            dynamoTable.put_item(
                Item={
                    "uuid": str(uuid.uuid1()),
                    "first_name": form.cleaned_data.get('first_name'),
                    "last_name": form.cleaned_data.get('last_name'),
                    "email": form.cleaned_data.get('email'),
                    "address": form.cleaned_data.get('address'),
                    "phone_number": form.cleaned_data.get('phone_number'),
                }
            )
            messages.success(request, f'You have successfully registered!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
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
    
    transactions = []
    results = dynamoTable_trans.scan()

    for result in results['Items']:
        if result['user_email'] == request.user.email:
            trans_id = result['uuid']
            trans_vendor_company_name = result['vendor_company_name']
            trans_vendor_email = result['vendor_email']
            trans_vendor_address = result['vendor_address']
            trans_vendor_website = result['vendor_website']
            trans_date = result['date']
            trans_amount = result['amount']
            trans = [
                trans_id, 
                trans_vendor_company_name,
                trans_vendor_email,
                trans_vendor_address,
                trans_vendor_website,
                trans_date,
                trans_amount
            ]
            transactions.append(trans)
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'transactions': transactions
    }
    return render(request, 'users/profile.html', context)

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

def trans(request):
    transactions = []
    results = dynamoTable_trans.scan()
    total_amount = 0
    for result in results['Items']:
        if result['user_email'] == request.user.email:
            trans_id = result['uuid']
            trans_vendor_company_name = result['vendor_company_name']
            trans_vendor_email = result['vendor_email']
            trans_vendor_address = result['vendor_address']
            trans_vendor_website = result['vendor_website']
            trans_date = result['date']
            trans_amount = result['amount']
            total_amount += result['amount']
            trans = [
                trans_id, 
                trans_vendor_company_name,
                trans_vendor_email,
                trans_vendor_address,
                trans_vendor_website,
                trans_date,
                trans_amount
            ]
            transactions.append(trans)
    context = {
        'transactions': transactions,
        'total_amount': total_amount
    }
    return render(request, 'users/trans.html', context)
