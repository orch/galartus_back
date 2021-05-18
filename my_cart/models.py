from django.db import models


class CartLine(models.Model):
    exhibition = models.ForeignKey('main.Exhibitions', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total = models.DecimalField(decimal_places=2, max_digits=14)

    @classmethod
    def create(cls, exhibition, quantity, total):
        cart_line = cls(exhibition=exhibition, quantity=quantity, total=total)
        return cart_line


class Cart(models.Model):
    items = models.ManyToManyField('CartLine')
    account = models.ForeignKey('users.NewUser', on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=14, default=0)
    is_ordered = models.BooleanField(default=False)

    def get_cart_items(self):
        return self.items

    def get_cart_amount(self):
        return sum([item.total for item in self.items.all()])
