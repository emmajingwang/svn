from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email=forms.EmailField()
    first_name=forms.CharField(max_length=20)
    last_name=forms.CharField(max_length=20)
    class Meta:
        model=User
        fields=['username', 'email', 'password1', 'password2']
 
PACKAGE_CHOICES=[('npm','NPM'),('nuget','NUGET'),]        
class InputForm(forms.Form):
    account = forms.CharField(label='SVN-Account', max_length=100)
    username=forms.CharField(label='Username', required=False,max_length=200)
    password=forms.CharField(label='Password',required=False, max_length=200)
    package=forms.CharField(label='Please choose the package used in your project', widget=forms.Select(choices=PACKAGE_CHOICES))
    email= forms.EmailField(label='Email Address', max_length = 200)
    project=forms.CharField(label='Project Name', max_length=200)
    branch_name=forms.CharField(label='Branch number', required=False, max_length=30)
     
REPORT_CHOICES= [('1', 'Everyday'),('7','Every Week'),]
  
class ScheduleForm(forms.Form):
    account = forms.CharField(label='SVN-Account', max_length=100)
    email= forms.CharField(label='Email Address', max_length = 200)
    choice=forms.CharField(label='How oftern would you like to receive your report?', widget=forms.Select(choices=REPORT_CHOICES))
        