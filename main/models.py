from django.db import models
# from django.dispatch import receiver
# import os


class Categories(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='content/categories')


class Pictures(models.Model):
    categories = models.ManyToManyField('Categories')
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True)
    image = models.ImageField(upload_to='content/pictures')


