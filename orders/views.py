from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from .models import Cart, CartItem
from orders.models import Order, OrderItem



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
            return redirect('products')

        total_price = cart.total_price

        if request.user.balance < total_price:
            messages.error(request, f"Mablag' yetarli emas. Balans: {request.user.balance}, Buyurtma: {total_price}")
            return redirect('checkout')

        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                username=request.user.username,
                phone=getattr(request.user, 'phone', ''),  # phone maydoni yo'q bo'lsa xato bermaydi
                address=getattr(request.user, 'address', ''),
                total_price=total_price,
                status='pending'
            )

            for item in cart.items.all():
                if item.product.stock < item.quantity:
                    messages.error(request, f"{item.product.title} mahsuloti omborda yetarli emas.")
                    raise Exception("Ombor yetishmovchiligi")  # Tranzaktsiyani bekor qilish uchun

                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.discount_price or item.product.price,
                    quantity=item.quantity,
                    product_title=item.product.title,
                    product_image=item.product.main_image
                )

                item.product.stock -= item.quantity
                item.product.save()

            request.user.balance -= total_price
            request.user.save()

            cart.is_ordered = True
            cart.save()

        messages.success(request, "Buyurtmangiz muvaffaqiyatli yaratildi va pul yechildi!")
        return redirect('order_success')




class OrderSuccessView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'order_success.html')


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

        if order.status == 'pending':
            with transaction.atomic():
                for item in order.items.all():
                    item.product.stock += item.quantity
                    item.product.save()

                order.status = 'cancelled'
                order.save()
                messages.success(request, "Buyurtma bekor qilindi.")
        else:
            messages.error(request, "Bu buyurtmani bekor qilib bolmaydi.")

        return redirect('order_detail', pk=pk)
