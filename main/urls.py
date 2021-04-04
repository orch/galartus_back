from django.urls import path
from . import views

urlpatterns = [
    path('categories', views.CategoriesListCreateView.as_view()),
    path('pictures', views.PicturesListCreateView.as_view()),
    path('categories/<int:pk>', views.CategoriesUpdateView.as_view()),
    path('pictures/<int:pk>', views.PicturesUpdateView.as_view()),
    path('categories/<int:pk>/delete', views.CategoriesDeleteView.as_view()),
    path('pictures/<int:pk>/delete', views.PicturesDeleteView.as_view()),
]
