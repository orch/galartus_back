from django.urls import path
from . import views

urlpatterns = [
    path('categories', views.CategoriesListView.as_view()),
    path('categories/create', views.CategoriesCreateView.as_view()),
    path('pictures', views.PicturesListView.as_view()),
    path('pictures/create', views.PicturesCreateView.as_view()),
    path('categories/<int:pk>', views.CategoriesUpdateView.as_view()),
    path('pictures/<int:pk>', views.PicturesUpdateView.as_view()),
    path('categories/<int:pk>/delete', views.CategoriesDeleteView.as_view()),
    path('pictures/<int:pk>/delete', views.PicturesDeleteView.as_view()),
]
