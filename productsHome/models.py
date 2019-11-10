from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
# Create your models here.
class Products(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField()
    views = models.IntegerField(null = True)
    image = models.ImageField(upload_to = 'productImages/')
    dateUploaded =  models.DateField(auto_now_add=True)
    Daytimestamp = models.DateField(auto_now_add=True)
    actualViews = models.IntegerField(null = True)

    class Meta:
        ordering = ['title']

class Views(models.Model):
    X = ArrayField(models.IntegerField(blank = True))
    # Y = ArrayField(models.DecimalField(blank = True,max_digits=2, decimal_places=2))
    Y = ArrayField(models.FloatField(blank= True))
    Viewtimestamp = models.DateTimeField(auto_now_add=True)
    

# class Dashboard(models.Model):
#     videoNumber = models.ForeignKey(Products, on_delete=models.CASCADE)
#     X = models.IntegerField(null = True)
#     Y = models.IntegerField(null = True)