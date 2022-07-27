
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
from .svn import svn
#from .schedule import task
import time, schedule
from .models import Scheduledtask

#############html page##################
def index(request):
    if request.method=='POST':
        form = InputForm(request.POST)
        if form.is_valid():
            repo=request.POST['account']
            email = request.POST['email']
            #results = svn(repo)
            svn(repo,email)   
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
           #repo=request.POST['account']
           #email = request.POST['email'] 
           #choice=int(request.POST['choice'])
           #task(svn(repo,email), choice)
           
            job = Scheduledtask.objects.create()
            job.account=request.POST['account']
            job.email=request.POST['email']
            job.frequency = request.POST['choice']
            job.save()
            
            #needs to be run in the backend!
            repo = job.account
            email = job.email
            choice=int(job.frequency)
            
           # return render(request,'user/report.html',{'account':repo, 'email':email,' choice':choice})
            if choice == 1:
                schedule.every(choice).day.at("14:17").do(svn,repo,email)
            else:
                schedule.every(choice).days.at("14:17").do(svn,repo,email)
            while True:
               schedule.run_pending()
               time.sleep(1)
             
            
    else:
        form = ScheduleForm()
    return render(request, 'user/task.html', {'form': form, 'title':'task'})
############## sign up page ###################
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            #username = form.cleaned_data.get('username')
            #email = form.cleaned_data.get('email')
            ######################### mail system #################################### 
            #htmly = get_template('user/Email.html')
            #d = { 'username': username }
            #subject, from_email, to = 'welcome', 'emma.wang@gov.bc.ca', email
            #html_content = htmly.render(d)
            #msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            #msg.attach_alternative(html_content, "text/html")
            #msg.send()
            ################################################################## 
            messages.success(request, f'Your account has been created ! You are now able to log in')
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

        