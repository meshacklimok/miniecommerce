from django.urls import path
from . import views

app_name = 'mpesapayment'

urlpatterns = [
    # Initiate STK Push for a specific order
    path('payment/initiate/<int:order_id>/', views.initiate_payment, name='initiate_payment'),

    # Callback URL that Safaricom will hit after payment
    path('payment/callback/', views.payment_callback, name='payment_callback'),

    # Optional test endpoint for standalone STK push
    path('stk_push/', views.initiate_stk_push, name='stk_push'),
]
