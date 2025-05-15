from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True)
    title = models.CharField( max_length=50)
    description = models.TextField(null = True, blank = True)    
    created = models.DateField(auto_now_add=True)
    due_date= models.DateField(null=True,blank=True)
    completed = models.BooleanField( default = False)

    def __str__(self):
        return self.title
    