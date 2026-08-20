from django.urls import path
from .views import ProductListView, ProductDetailView, add_to_cart, cart_view, remove_from_cart, update_cart

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('product/<int:product_id>/add-to-cart/', add_to_cart, name='add-to-cart'),
    path('cart/', cart_view, name='cart'),
    path(
        'cart/update/<int:product_id>/increase/',
        update_cart,
        {'action': 'increase'},
        name='increase-cart',
    ),
    path(
        'cart/update/<int:product_id>/decrease/',
        update_cart,
        {'action': 'decrease'},
        name='decrease-cart',
    ),
    path(
        'cart/remove/<int:product_id>/',
        remove_from_cart,
        name='remove-from-cart',
    ),
]