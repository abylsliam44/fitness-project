from django.urls import path
from .views import (
    ProductListView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ProductDetailView
)

urlpatterns = [
    path('', ProductListView.as_view(), name='marketplace'),
    path('add/', ProductCreateView.as_view(), name='product_add'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('edit/<slug:slug>/', ProductUpdateView.as_view(), name='product_update'),
    path('delete/<slug:slug>/', ProductDeleteView.as_view(), name='product_delete'),
]