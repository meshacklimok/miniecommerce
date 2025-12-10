from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    # Homepage
    path('', views.home, name='home'),

    # Products listing and details
    path('products/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    # Admin actions
    path('product/add/', views.add_product, name='add_product'),
    path('product/update/<int:product_id>/', views.update_product, name='update_product'),
    path('product/delete/<int:product_id>/', views.delete_product, name='delete_product'),

    # Wishlist toggle
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
]
