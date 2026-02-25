from django.test import TestCase

# ====Model===
# 1)Product bunga view va field larini qo'shib yuboring
# 2)Wishlis
# 3)Category faqat admin qo'sha oladigan qilish kerak yani user qo'shmaydi
# ======view====
# 10Product Crud qismi
# 2)wishlis crud
# 3)product nechta odam olgani oxirgi haftada malumoti ko'rinsin
# orders dan malumot olinadi
# 4) nechta odam olmoqchi yani nechat odamni karzinkasida turibdi
# 3 bilan yangi funksiya kim yana qo'shimcha qilmoqchi bo'lsa aytsin

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Category, Products

class ProductTest(TestCase):
    def test_create_and_discount(self):
        # 1. Tayyorgarlik (User va Kategoriya)
        user = get_user_model().objects.create_user('test', 'test@a.com', '1')
        cat = Category.objects.create(name="Cat")
        self.client.login(username='test', password='1')

        # 2. Post so'rovi (Eng muhim ma'lumotlar bilan)
        data = {
            'category': cat.id, 'title': 'P', 'brand': 'B',
            'price': '100', 'percent': '20', 'stock': '1', 'desc': 'D'
        }
        res = self.client.post(reverse('product_create'), data=data)

        # 3. Tekshiruv (Redirect va 100 - 20% = 80)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(Products.objects.get().discount_price, 80)