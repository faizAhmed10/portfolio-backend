from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Website(models.Model):
    image = models.ImageField(upload_to="SiteImg", null=True, blank=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    built_with = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    github_link = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.title

class Testimonials(models.Model):
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    _id = models.AutoField(primary_key = True, editable = False)
    def __str__(self):
        return self.name
    

    