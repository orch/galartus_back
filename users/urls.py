from django.urls import path
from . import views

urlpatterns = [
    path('register', views.UsersView.as_view(), name='users'),
    path('logout', views.BlackListView.as_view(), name='users'),
    path('', views.UsersListView.as_view()),
    path('<int:pk>/delete', views.UsersView.as_view(), name='main'),
    path('<int:pk>', views.UsersView.as_view(), name='main'),
]