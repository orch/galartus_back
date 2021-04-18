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


class Exhibitions(models.Model):
    categories = models.ManyToManyField('Categories')
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000, null=True)
    image = models.ImageField(upload_to='content/exhibition')
    date = models.DateField()
    time = models.TimeField()
    price = models.DecimalField(decimal_places=2, max_digits=8)
    address = models.CharField(max_length=250)
    weekday = models.IntegerField(null=True)


class Accounts(models.Model):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    birthday = models.DateField(null=True)
    nick_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='content/account', null=True)


class Likes(models.Model):
    picture = models.ForeignKey('Pictures', on_delete=models.CASCADE)
    account = models.ForeignKey('Accounts', on_delete=models.CASCADE)


