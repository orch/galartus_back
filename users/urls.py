from django.urls import path
from . import views

urlpatterns = [
    path('register', views.UsersView.as_view(), name='users'),

]