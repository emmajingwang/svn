
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import InputForm, ScheduleForm, UserRegisterForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from .solution import svn
import time, schedule
from .models import Scheduledtask 

#############html page##################
def index(request):
    if request.method=='POST':
        form = InputForm(request.POST)
        if form.is_valid():
            repo=request.POST['account']
            email = request.POST['email']
            username=request.POST['username']
            password=request.POST['password']
            package=request.POST['package']
            project=request.POST['project']
            branchNum=request.POST['branch_name']
        
            svn(repo,username,password,package,email,project,branchNum)
            #svn(repo,email,package,project,branchNum)
        return render(request, 'user/report.html', {'title': 'report'})  
    
    else:
        form=InputForm()
        return render(request, 'user/index.html', {'form': form, 'title': 'index'})

############### report page#############
def report(request):
    return render(request, 'user/report.html', {'title':'report'})

######## schedule page ######
def task(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():   
            #create an object and assign value to the properties
            job = Scheduledtask.objects.create()
            job.account=request.POST['account']
            job.username=request.POST['username']
            job.password=request.POST['password']
            job.email=request.POST['email']
            job.package=request.POST['package']
            job.project=request.POST['project']
            job.frequency = request.POST['choice']
            job.branchNum=request.POST['branch_name']
            job.save()
            
            account= job.account
            username=job.username
            password=job.password
            package=job.package
            project=job.project
            branchNum=job.branchNum
            email = job.email
            choice=int(job.frequency)
            
            
            if choice == 1:
                schedule.every(choice).day.at("13:55").do(svn,account,username,password,package,email,project,branchNum)
            else:
                schedule.every(choice).days.at("14:17").do(svn,username,password,package,email,project,branchNum)
            while True:
               schedule.run_pending()
               time.sleep(60)
             
            
    else:
        form = ScheduleForm()
    return render(request, 'user/task.html', {'form': form, 'title':'task'})
############## sign up page ###################
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form, 'title':'register here'})
######################### login forms#######################
def Login(request):
    if request.method=='POST':
        #AuthenticationForm_can_also_be_used__
        
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            form = login (request, user)
            messages.success(request, f' welcome')
            return redirect('index')
        else:
            messages.info(request, f'account not exists')
    form = AuthenticationForm()
    return render(request, 'user/login.html',  {'form':form, 'title':'log in'})

        