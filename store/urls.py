from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('product/<slug:slug>',views.product_detail,name='product_detail'),
    path('cart/',views.cart,name='cart'),
    path('add_to_cart/<slug:slug>', views.add_to_cart,name='add_to_cart'),
    path('remove_from_cart/<slug:slug>', views.remove_from_cart,name='remove_from_cart'),
    path('increase-quantity/<slug:slug>/',views.increase_quantity,name='increase_quantity'),
    path('checkout/',views.checkout,name='checkout'),
    path('order-success/',views.order_success,name='order_success'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('account/', views.account, name='account'),
    path('', views.home, name='home'),
    path('category/<slug:slug>/',views.category_products,name='category_products'),
    path('product/<slug:slug>',views.product_detail,name='product_detail'),
]