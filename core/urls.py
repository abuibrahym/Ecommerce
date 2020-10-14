from django.urls import path
from . import views
app_name = 'core'
urlpatterns = [
    path('', views.item_list, name='home'),
    path('checkout/', views.checkout, name='checkout'),
    path('delete/<int:pk>', views.delete, name='delete'),
    path('charge_base/', views.charge_base, name="charge_base"),
    path('charge/', views.charge, name="charge"),
    path('favorites/', views.FavoritesView.as_view(), name='favorites'),
    path('order-summary/', views.OrderSummaryView.as_view(), name='order-summary'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add-to-cart'),
    path('add-to-favorites/<int:pk>/', views.add_to_favorites, name='add-to-favorites'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove-from-cart'),
    path('payment/<payment_option>', views.PaymentView.as_view(), name='payment'),
]
