from random import choices
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
        
class InputForm(forms.Form):
    account = forms.CharField(label='SVN-Account', max_length=100)
    email= forms.CharField(label='Email Address', max_length = 200)
 
REPORT_CHOICES= [('1', 'Everyday'),('7','Every Week'),]
  
class ScheduleForm(forms.Form):
    account = forms.CharField(label='SVN-Account', max_length=100)
    email= forms.CharField(label='Email Address', max_length = 200)
    choice=forms.CharField(label='How oftern would you like to receive your report?', widget=forms.Select(choices=REPORT_CHOICES))
        