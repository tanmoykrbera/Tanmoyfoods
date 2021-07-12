from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from core.customer import forms

from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from core.models import *




@login_required()
def home(request):
    return redirect(reverse('customer:profile'))

@login_required(login_url="/sign-in/?next=/customer/")
def profile_page(request):

    user_form = forms.BasicUserForm(instance=request.user)
    customer_form = forms.BasicCustomerForm(instance=request.user.customer)
    password_form = PasswordChangeForm(request.user)


    if request.method == "POST":
        
        if request.POST.get('action') == 'update_profile':
            user_form = forms.BasicUserForm(request.POST, instance=request.user)
            customer_form = forms.BasicCustomerForm(request.POST, request.FILES, instance=request.user.customer)

            if user_form.is_valid() and customer_form.is_valid():
                user_form.save()
                customer_form.save()

                messages.success(request, 'Your profile has been updated')
                return redirect(reverse('customer:profile'))

        elif request.POST.get('action') == 'update_password':
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)

                messages.success(request, 'Your password has been updated')
                return redirect(reverse('customer:profile'))
                    


    return render(request, 'customer/profile.html', {
        "user_form": user_form,
        "customer_form":customer_form,
        "password_form":password_form


    })


@login_required(login_url="/sign-in/?next=/customer/")
def payment_method_page(request):
    current_customer= request.user.customer


    return render(request, 'customer/payment_method.html')


@login_required(login_url="/sign-in/?next=/customer/")
def create_job_page(request):

    current_customer = request.user.customer
        

    creating_job= Job.objects.filter(customer= current_customer, status = Job.CREATING_STATUS).last()
    step1_form = forms.JobCreateStep1Form(instance = creating_job)
    step2_form = forms.JobCreateStep2Form(instance = creating_job)
    step3_form = forms.JobCreateStep3Form(instance = creating_job)

    if request.method == "POST":
        if request.POST.get('step') == '1':
            step1_form = forms.JobCreateStep1Form(request.POST, request.FILES, instance = creating_job)
            if step1_form.is_valid():
                creating_job = step1_form.save(commit=False)
                creating_job.customer = current_customer
                creating_job.save()
                return redirect(reverse('customer:create_job'))
        elif request.POST.get('step') == '2':
            step2_form = forms.JobCreateStep2Form(request.POST, instance=creating_job)
            if step2_form.is_valid():
                creating_job = step2_form.save()
                return redirect(reverse('customer:create_job'))
        elif request.POST.get('step') == '3':
            step3_form = forms.JobCreateStep3Form(request.POST, instance=creating_job)
            if step3_form.is_valid():
                creating_job = step3_form.save()               
     
     # Determine the current step
    if not creating_job:
        current_step = 1
    elif creating_job.delivery_name:
        current_step = 4    
    
    elif creating_job.pickup_name:
        current_step = 3    
    
    else:
        current_step = 2


    return render(request, 'customer/create_job.html',{
        
        "job": creating_job,
        "step": current_step,
        "step1_form": step1_form,
        "step2_form": step2_form,
        "step3_form": step3_form,
    })
def current_jobs_page(request):
    jobs = Job.objects.filter(
        customer=request.user.customer,
        status__in=[
            Job.PROCESSING_STATUS,
            Job.PICKING_STATUS,
            Job.DELIVERING_STATUS
        ]
    )

    return render(request, 'customer/jobs.html', {
        "jobs": jobs
    })

@login_required(login_url="/sign-in/?next=/customer/")
def archived_jobs_page(request):
    jobs = Job.objects.filter(
        customer=request.user.customer,
        status__in=[
            Job.COMPLETED_STATUS,
            Job.CANCELED_STATUS
        ]
    )

    return render(request, 'customer/jobs.html', {
        "jobs": jobs
    })    
