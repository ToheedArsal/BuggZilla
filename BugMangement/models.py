from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


# Create your models here.
class CustomUser(User):
    USER_TYPE_CHOICES=[
    ("manager", "manager"),
    ("developer", "developer"),
    ("qa", "qa"),
    ]
    user_type= models.CharField( max_length = 20, choices =  USER_TYPE_CHOICES, default = "manager")

    def __str__(self):
        return self.username
    
class Project(models.Model):

    project_name=models.CharField(max_length=50)
    project_description = models.TextField()
    developer = models.ManyToManyField(CustomUser, related_name='projects', null=True, blank=True)
    qa = models.ManyToManyField(CustomUser, null=True, blank=True)
    managers = models.ForeignKey(CustomUser, related_name='managed_projects', on_delete=models.CASCADE, null=True,blank=True)

    def __str__(self):
        return self.project_name

class Bug(models.Model):

    BUG_TYPES = [
        ('feature', 'feature'),
        ('bug', 'bug'),
    ]

    BUG_STATUS = [
        ('new', 'new'),
        ('started', 'started'),
        ('completed' ,'completed'),
        ('resolved', 'resolved'),
    ]


    bug_title=models.CharField(max_length=50, unique=True)
    bug_description = models.TextField(blank=True)
    deadline = models.DateField(blank=True, null=True)
    screenshot=CloudinaryField('image',blank=True, null=True)
    bug_type = models.CharField(max_length=20, choices=BUG_TYPES, default="bug")
    status = models.CharField(max_length=20, choices=BUG_STATUS, default="new")
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_bugs')
    developer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assigned_bugs', null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='bugs')

    def __str__(self):
        return self.bug_title


