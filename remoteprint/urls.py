from django.urls import path
from remoteprint.views import *

app_name = 'remoteprint'

urlpatterns = [
    path('mypage/', print_mypage, name='mypage'),
    path('payment_detail/', print_payment_detail, name='payment_detail'),
    path('cancel_order/<int:order_id>/', print_cancel_order, name='cancel_order'),
]