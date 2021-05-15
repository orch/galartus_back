from django.db import models
from django.conf import settings


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


class Likes(models.Model):
    picture = models.ForeignKey('Pictures', on_delete=models.CASCADE)
    account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class CartLine(models.Model):
    exhibition = models.ForeignKey('Exhibitions', on_delete=models.CASCADE)
    quantity = models.IntegerField()


class Cart(models.Model):
    cart_line = models.ForeignKey('CartLine', on_delete=models.CASCADE)
    # account = models.ForeignKey('NewUser', on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=14)




