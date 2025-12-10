from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Customer dashboard
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),

    # Profile update
    path('profile/update/', views.update_customer_profile, name='update_profile'),

    # Cancel order
    path('order/cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),

    # Customer orders
    path('orders/', views.order_history, name='order_history'),

    # Password change
    path('password/change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('password/change/done/', views.CustomPasswordChangeDoneView.as_view(), name='password_change_done'),

    # Password reset
    path('password/reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password/reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password/reset/confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/reset/complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
