from django.contrib import admin
from .models import Categories, Pictures, Exhibitions, Likes #, Accounts
# Register your models here.


admin.site.register(Categories)
admin.site.register(Pictures)
admin.site.register(Exhibitions)
# admin.site.register(Accounts)
admin.site.register(Likes)
