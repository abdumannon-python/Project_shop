from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from .models import Cart, CartItem
from orders.models import Order, OrderItem
from products.models import Products
from users.models import Comment


class CheckoutView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        cart = Cart.objects.filter(user=request.user, is_ordered=False).first()
        if not cart or not cart.items.exists():
            messages.info(request, "Savat bo'sh.")
            return redirect('products')

        total_price = cart.total_price
        return render(request, 'checkout.html', {
            'cart': cart,
            'total_price': total_price,
        })

    def post(self, request):
        cart = Cart.objects.filter(user=request.user, is_ordered=False).first()
        if not cart or not cart.items.exists():
            messages.error(request, "Savat bo'sh, buyurtma berib bo'lmaydi.")
            return redirect('home')

        total_price = cart.total_price

        if request.user.balance < total_price:
            messages.error(request, f"Mablag' yetarli emas. Balans: {request.user.balance}, Buyurtma: {total_price}")
            return redirect('checkout')

        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                username=request.user.username,
                phone=getattr(request.user, 'phone', ''),
                address=getattr(request.user, 'address', ''),
                total_price=total_price,
                status='pending'
            )

            for item in cart.items.all():
                if item.product.stock < item.quantity:
                    messages.error(request, f"{item.product.title} mahsuloti omborda yetarli emas.")
                    raise Exception("Ombor yetishmovchiligi")
                product=item.product
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=product.discount_price or product.price,
                    quantity=item.quantity,
                    product_title=product.title,
                    product_image=product.main_image
                )

                product.stock -= item.quantity
                product.save()
                seller=product.auth
                seller.balance+=total_price
                seller.save()
            request.user.balance -= total_price
            request.user.save()

            cart.is_ordered = True
            cart.save()

        messages.success(request, "Buyurtmangiz muvaffaqiyatli yaratildi va pul yechildi!")
        return render(request, 'order_success.html', {'order': order})


class OrderListView(LoginRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'order_list.html', {'orders': orders})


class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        order = get_object_or_404(Order, id=pk, user=request.user)
        items = order.items.all()

        return render(request, 'order_detail.html', {
            'order': order,
            'items': items
        })

class OrderCancelView(LoginRequiredMixin, View):
    def post(self, request, pk):
        order = get_object_or_404(Order, id=pk, user=request.user)
        User=request.user
        if order.status == 'pending':
            with transaction.atomic():
                for item in order.items.all():
                    product=item.product
                    product.stock += item.quantity
                    product.save()
                    seller = product.auth
                    seller.balance -= order.total_price
                    User.balance+=order.total_price
                    User.save()
                    seller.save()

                    item.product.save()

                order.status = 'cancelled'
                order.save()
                messages.success(request, "Buyurtma bekor qilindi.")
        else:
            messages.error(request, "Bu buyurtmani bekor qilib bolmaydi.")

        return redirect('order_detail', pk=pk)


class AddCartView(LoginRequiredMixin,View):
    def post(self,request,pk):
        product=get_object_or_404(Products,pk=pk)
        cart,created=Cart.objects.get_or_create(user=request.user,is_ordered=False)

        cart_item,item_created=CartItem.objects.get_or_create(cart=cart,product=product)

        if not item_created:
            cart_item.quantity+=1
            cart_item.save()

        return redirect('cart_view')

class CartView(LoginRequiredMixin,View):
    def get(self,request):
        cart=Cart.objects.filter(user=request.user,is_ordered=False).first()
        if cart:
            cart_count = cart.items.count()
        else:
            cart_count = 0
        return render(request,'cart.html',{'cart':cart,'cart_count':cart_count})


class RemoveFromCartView(LoginRequiredMixin,View):
    def post(self,request,id):
        product=get_object_or_404(Products,id=id)
        cart=Cart.objects.get(user=request.user,is_ordered=False)
        cart_item=CartItem.objects.filter(cart=cart,product=product).first()
        if not cart_item:
            return redirect('cart_view')
        if cart_item.quantity>1:
            cart_item.quantity-=1
            cart_item.save()
        else:
            cart_item.delete()

        return redirect('cart_view')
class DeleteCart(LoginRequiredMixin,View):
    def post(self,request,product_id):
        cart=Cart.objects.get(user=request.user,is_ordered=False)
        CartItem.objects.filter(cart=cart,product_id=product_id).delete()
        return redirect('cart_view')

class CommentUpdate(LoginRequiredMixin,View):
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id, user=request.user)
        products = comment.post
        return render(request, 'comment_update.html', {'comment': comment,
                                                       'products': products
                                                       })
    def post(self,request, comment_id):
        comment=get_object_or_404(Comment,id=comment_id,user=request.user)
        text=request.POST.get('text')
        if text:
            comment.text=text
            comment.save()
            messages.success(request, "Sharh yangilandi")
            return redirect('product_detail', pk=comment.post.pk)
        return render(request, 'comment_update.html', {'comment': comment, 'products': comment.post})


class CommentDelete(LoginRequiredMixin,View):
    def post(self,request,comment_id):
        comment = get_object_or_404(Comment,id=comment_id,user=request.user)
        comment.delete()
        messages.success(request, "Sharh o‘chirildi")
        return redirect('product_detail', pk=comment.post.pk)

class OrderStatusView(LoginRequiredMixin,View):
    def get(self,request):
        order=OrderItem.objects.filter(product__auth=request.user).select_related('order','product')
        context={
            'order':order
        }
        return render(request,'orders.html',context)
    def post(self,request):
        order_item_id=request.POST.get('order_item_id')
        new_status=request.POST.get('status')
        orderitem=get_object_or_404(OrderItem,id=order_item_id,product__auth=request.user)
        seller=request.user
        order=orderitem.order
        user=order.user
        if new_status in dict(Order.STATUS_CHOICES).keys():
            old_status = order.status
            if new_status=='cancelled':
                for item in order.items.all():
                    product = item.product
                    product.stock += item.quantity

                    seller.balance -= order.total_price
                    user.balance+=order.total_price
                    user.save()
                    seller.save()
                    product.save()
            order.status=new_status
            order.save()
            messages.success(
                request,
                f"Buyurtma #{order.id} holati '{old_status}' dan '{new_status}' ga o'zgartirildi!"
            )
        else:
            messages.error(request, "Noto'g'ri holat tanlandi!")

        return redirect("order_detail")



    