from django.urls import path

from .views import *



urlpatterns=[
    path('',ProductView.as_view(),name='home'),
    path('dashboard/',DashboardView.as_view(),name='dashboard'),
    path('product/create/', ProductCreate.as_view(), name='product_create'),
    path('product/update/<int:pk>/',ProductUpdate.as_view(),name='product_update'),
    path('product/detail/<int:pk>/',ProductDetails.as_view(),name='product_detail'),
    path('product/delete/<int:pk>/', ProductDelete.as_view(), name='product_delete'),
    path('wishlist/<int:id>/',WishesView.as_view(),name='wishlist'),
    path('addwishlist/<int:pk>/',Addwish.as_view(),name='addwishlist'),
    path('chat/<int:chat_id>/', ChatDetail.as_view(), name='chat_detail'),
    path('chat/create/<int:recipient_id>/', ChatCreate.as_view(), name='chat_create'),
    path('message-update/<int:message_id>/',MessageUpdate.as_view(),name='message-update'),
    path('message-delete/<int:message_id>/',MessageDelete.as_view(),name='message-delete'),
    path('chatlist/',ChatView.as_view(),name='chat_list')
]