from django.urls import path
from .views import *
urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('my-orders/', OrderListView.as_view(), name='order_list'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('order/<int:pk>/cancel/', OrderCancelView.as_view(), name='order_cancel'),
    path('addcart/<int:pk>',AddCartView.as_view(),name='addcart'),
    path('cartview/', CartView.as_view(), name='cart_view'),
    path('cartremove/<int:id>', RemoveFromCartView.as_view(), name='cartremove'),
    path('cartdelete/<int:product_id>',DeleteCart.as_view(),name='cartdelete'),
    path('comment/update/<int:comment_id>/',CommentUpdate.as_view(),name='comment_update'),
    path('comment/delete/<int:comment_id>/',CommentDelete.as_view(),name='comment_delete'),
]