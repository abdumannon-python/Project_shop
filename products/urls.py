from django.urls import path

from .views import *



urlpatterns=[
    path('',ProductView.as_view(),name='home'),
    path('product/create/', ProductCreate.as_view(), name='product_create'),
    path('product/update/<int:pk>/',ProductUpdate.as_view(),name='product_update'),
    path('product/detail/<int:pk>/',ProductDetails.as_view(),name='product_detail'),
    path('wishlist/<int:id>/',WishesView.as_view(),name='wishlist'),
    path('addwishlist/<int:id>/',Addwish.as_view(),name='addwishlist'),
    path('chat/<int:chat_id>/', ChatDetail.as_view(), name='chat_detail'),
    path('start-chat/<int:recipient_id>/', ChatCreate.as_view(), name='start_chat'),
    path('message-update/<int:message_id>/',MessageUpdate.as_view(),name='message-update'),
    path('message-delete/<int:message_id>/',MessageDelete.as_view(),name='message-delete'),
]