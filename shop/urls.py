from django.urls import path
from shop.views import *

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('cart/', cart, name='cart'),
    path('add/<int:id>/', add_to_cart, name='add_to_cart'),
    path('remove/<int:id>/', remove_from_cart, name='remove_from_cart'),
    path('payment/', payment, name='payment'),

]
