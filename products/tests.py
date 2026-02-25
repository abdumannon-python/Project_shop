
# ====Model===
# 1)Product bunga view va field larini qo'shib yuboring
# 2)Wishlis
# 3)Category faqat admin qo'sha oladigan qilish kerak yani user qo'shmaydi
# ======view====
# 10 Product Crud qismi
# 2)wishlis crud
# 3)product nechta odam olgani oxirgi haftada malumoti ko'rinsin
# orders dan malumot olinadi
# 4) nechta odam olmoqchi yani nechat odamni karzinkasida turibdi
# 3 bilan yangi funksiya kim yana qo'shimcha qilmoqchi bo'lsa aytsin
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase
class ProductTest(TestCase):
    def test_create_and_discount(self):

        user = get_user_model().objects.create_user(username='test', password='1')
        cat = Category.objects.create(title="Elektronika")
        self.client.login(username='test', password='1')

        data = {
            'category': cat.id,
            'title': 'iPhone',
            'brand': 'Apple',
            'price': '1000',
            'percent': '10',
            'stock': '10',
            'desc': 'Yangi telefon'
        }


        url = '/products/product/create/'

        res = self.client.post(url, data=data)


        self.assertEqual(res.status_code, 302)

        product = Products.objects.get(title='iPhone')
        self.assertEqual(product.discount_price, 900)


from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Products, Category, ProductImages




class ProductUpdateTest(TestCase):
    def setUp(self):
        # 1. Tayyorgarlik: User, Kategoriya va Mahsulot yaratish
        self.user = get_user_model().objects.create_user('test', 't@a.com', '1')
        self.cat = Category.objects.create(title="Eski")  # Category modeli 'title' ishlatadi
        self.new_cat = Category.objects.create(title="Yangi")

        self.product = Products.objects.create(
            auth=self.user, category=self.cat, title="Eski Nom",
            brand="B", price=100, stock=1, desc="D"
        )
        self.client.login(username='test', password='1')
        # URL nomini urls.py dagi 'name' bilan moslang (masalan: 'product_update')
        self.url = reverse('product_update', kwargs={'pk': self.product.pk})

    def test_update_success(self):
        # 2. Yangi ma'lumotlar yuborish
        data = {
            'category': self.new_cat.id,
            'title': 'Yangi Nom',
            'brand': 'New Brand',
            'price': '200',
            'present': '50',  # Sizda foiz 'present' nomi bilan kelyapti
            'stock': '10',
            'desc': 'Yangi tavsif'
        }
        res = self.client.post(self.url, data=data)

        # 3. Tekshiruvlar
        self.assertEqual(res.status_code, 302)  # Redirect bo'lishi kerak

        # Bazadan yangilangan mahsulotni qayta yuklaymiz
        self.product.refresh_from_db()

        self.assertEqual(self.product.title, 'Yangi Nom')
        self.assertEqual(self.product.category, self.new_cat)
        # 200 - 50% = 100. discount_price to'g'ri hisoblanganini tekshiramiz
        self.assertEqual(self.product.discount_price, 100)

    def test_update_permission(self):
        """Boshqa user mahsulotini o'zgartira olmasligini tekshirish (404 kutamiz)"""
        other_user = get_user_model().objects.create_user('hacker', 'h@a.com', '1')
        self.client.login(username='hacker', password='1')
        res = self.client.post(self.url, data={'title': 'Hacked'})
        self.assertEqual(res.status_code, 404)