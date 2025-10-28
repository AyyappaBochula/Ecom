from django.urls import path
from app1 import views
urlpatterns=[
    path('',views.home,name='home'),
     path('category/<str:category_name>/', views.category_products, name='category_products'),
    path('product/<int:pid>/<str:category>/',views.view_product,name='view_product'),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.logout,name='logout'),
    path('cart/',views.cart,name='cart'),
    path('add_cart/<int:pid>',views.add_cart,name='add_cart'),
    path('del_cart/<int:pid>/<str:size>',views.del_cart,name='del_cart'),
    path('profile/',views.profile,name='profile'),
    path('buy/',views.buy,name='buy'),
    path('buy_one/<int:pid>/<str:size>',views.buy_one,name='buy_one'),
    path('about/',views.about,name='about'),
]