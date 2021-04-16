from django.urls import path
from . import views

urlpatterns = [
    path('categories', views.CategoriesListView.as_view()),
    path('categories/create', views.CategoriesView.as_view(), name='main'),
    path('categories/<int:pk>', views.CategoriesView.as_view(), name='main'),
    path('categories/<int:pk>/delete', views.CategoriesView.as_view(), name='main'),

    path('pictures', views.PicturesListView.as_view()),
    path('pictures/create', views.PicturesView.as_view(), name='main'),
    path('pictures/<int:pk>', views.PicturesView.as_view(), name='main'),
    path('pictures/<int:pk>/delete', views.PicturesView.as_view(), name='main'),

    path('exhibition', views.ExhibitionsListView.as_view()),
    path('exhibition/create', views.ExhibitionsView.as_view(), name='main'),
    path('exhibition/<int:pk>', views.ExhibitionsView.as_view(), name='main'),
    path('exhibition/<int:pk>/delete', views.ExhibitionsView.as_view(), name='main'),
]
