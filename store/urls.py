from django.urls import path
from .views import ProductListView, ProductDetailView, add_to_cart

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('product/<int:product_id>/add-to-cart/', add_to_cart, name='add-to-cart'),
]