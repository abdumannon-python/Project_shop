from django.urls import path

from .views import (ProductCreate,
        ProductUpdate,ProductDetails,
        ProductView,
)



urlpatterns=[
    path('product/create/', ProductCreate.as_view(), name='product_create'),
    path('product/update/<int:pk>/',ProductUpdate.as_view(),name='product_update'),
    path('product/detail/<int:pk>/',ProductDetails.as_view(),name='product_detail'),
    path('products/view/',ProductView.as_view(),name='product_view'),
]