from django.urls import path
from .views import CartView, CartListView, CartPaymentView

urlpatterns = [
    path('add/<int:pk>/<int:quantity>', CartView.as_view(), name='add_to_cart'),
    path('details', CartListView.as_view(), name='order_details'),
    path('<int:item_id>/remove', CartView.as_view(), name='remove_from_cart'),
    path('payment', CartPaymentView.as_view(), name='payment'),
]