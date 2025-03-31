from django.urls import path
from .views import (
    ProductListView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ProductDetailView,
    AddToFavoritesView, 
    RemoveFromFavoritesView,
    FavoriteListView
)

urlpatterns = [
    path('', ProductListView.as_view(), name='marketplace'),
    path('add/', ProductCreateView.as_view(), name='product_add'),
    path('favorites/', FavoriteListView.as_view(), name='favorites'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('edit/<slug:slug>/', ProductUpdateView.as_view(), name='product_update'),
    path('delete/<slug:slug>/', ProductDeleteView.as_view(), name='product_delete'),
    path('favorites/add/<int:product_id>/', AddToFavoritesView.as_view(), name='add_to_favorites'),
    path('favorites/remove/<int:product_id>/', RemoveFromFavoritesView.as_view(), name='remove_from_favorites'),
]