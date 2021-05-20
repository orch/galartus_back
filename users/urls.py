from django.urls import path
from . import views

urlpatterns = [
    path('register', views.UsersView.as_view(), name='users'),
    path('logout', views.BlackListView.as_view(), name='users'),
    path('', views.UsersView.as_view(), name='users'),
    path('<int:pk>/delete', views.UsersView.as_view(), name='users'),
    path('<int:pk>', views.UsersView.as_view(), name='users'),
    path('recommendation', views.RecommendationView.as_view(), name='users')
]