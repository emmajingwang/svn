from django.db import models

# Create your models
class Scheduledtask(models.Model):
    account=models.CharField(max_length=200)
    email=models.EmailField()
    frequency = models.CharField(max_length=200)
    

        
   
        
    
    
    