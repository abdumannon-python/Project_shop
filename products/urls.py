from django.urls import path

from .views import ProductCreate

urlpatterns=[
    path('product_create/',ProductCreate.as_view(),name='create'),

]