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

    path('exhibitions', views.ExhibitionsListView.as_view()),
    path('exhibitions/create', views.ExhibitionsView.as_view(), name='main'),
    path('exhibitions/<int:pk>', views.ExhibitionsView.as_view(), name='main'),
    path('exhibitions/<int:pk>/delete', views.ExhibitionsView.as_view(), name='main'),

    path('likes', views.LikesListView.as_view()),
    path('likes/create', views.LikesView.as_view(), name='main'),
    path('likes/<int:pk>/delete', views.LikesDeleteView.as_view()),
]

# path('accounts', views.AccountsListView.as_view()),
# path('accounts/create', views.AccountsView.as_view(), name='main'),
# path('accounts/<int:pk>', views.AccountsView.as_view(), name='main'),
# path('accounts/<int:pk>/delete', views.AccountsView.as_view(), name='main'),
