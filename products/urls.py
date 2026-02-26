from django.urls import path

from .views import *



urlpatterns=[
    path('',ProductView.as_view(),name='home'),
    path('product/create/', ProductCreate.as_view(), name='product_create'),
    path('product/update/<int:pk>/',ProductUpdate.as_view(),name='product_update'),
    path('product/detail/<int:pk>/',ProductDetails.as_view(),name='product_detail'),
    path('wishlist/<int:id>/',WishesView.as_view(),name='wishlist'),
    path('addwishlist/<int:id>/',Addwish.as_view(),name='addwishlist'),
]