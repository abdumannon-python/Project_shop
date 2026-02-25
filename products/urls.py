from django.urls import path

from .views import ProductCreate,ProductUpdate

urlpatterns=[
    path('product/create/', ProductCreate.as_view(), name='product_create'),
    path('product/update/<int:pk>/',ProductUpdate.as_view(),name='product_update')
]