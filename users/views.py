import random
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from .models import *
from products.models import *
from decimal import Decimal, InvalidOperation

def generate():
    return ''.join([str(random.randint(0,9)) for i in range(6)])

class Register(View):
    def get(self, request):
        return render(request, 'auth/register.html')
    
    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        profile_image = request.FILES.get('profile_image')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        
        if password != confirm_password:
            return render(request, 'auth/register.html', {""
                "error": "Parollar mos Emas"
            })
        if len(password) < 5 or password is None:
            return render(request, 'auth/register.html', {
                "error": "Parol 5 ta belgidan kam yoki Parol Kiritilmagan"
            })
        if User.objects.filter(username=username).exists():
            return render(request, 'auth/register.html', {
                "error": "Bu Username allaqachon mavjud"
            })
        if User.objects.filter(email=email).exists():
            return render(request, 'auth/register.html', {
                "error": "Bu email allaqachon mavjud"
            })
        if profile_image.endwidth('.webp'):
            return render(request, 'auth/register.html', {
                "error": "Bu Formatdagi rasmlar mos kelmaydi"
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            profile_image = profile_image,
            password=password,
            is_activate = False
        )

        code = generate()

        Emailcode.objects.create(
            users=user,
            code=code
        )

        send_mail(
            'Tasdiqlash kodi',
            f'Sizning tasdiqlash kodingiz: {code}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False
        )
        request.session['temp_user_id'] = user.id
        return redirect('verify')
class VerifyPage(View):
    def get(self, request):
        return render(request, 'auth/email_verify.html')

    def post(self, request):
        code = request.POST.get('code')
        user_id = request.session.get('temp_user_id')

        if not user_id:
            return redirect('register')

        try:
            email_obj = Emailcode.objects.get(users_id=user_id, code=code)
            if email_obj.is_valid():
                user = email_obj.users
                user.is_active = True
                user.save()
                email_obj.delete()
                return redirect('login')
            else:
                return render(request, 'auth/email_verify.html', {'error': 'Kod vaqti o‘tgan!'})
        except Emailcode.DoesNotExist:
            return render(request, 'auth/email_verify.html', {'error': 'Noto‘g‘ri kod!'})

class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html', {'username': ''})

    def post(self, request):
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            return render(request, 'auth/login.html', {
                'error': 'Username va parol kiritilishi shart!',
                'username': username
            })

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'auth/login.html', {
                    'error': 'Hisobingiz faol emas!',
                    'username': username
                })
        else:
            return render(request, 'auth/login.html', {
                'error': 'Username yoki parol xato!',
                'username': username
            })

class Profile(View):
    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        products = Products.objects.filter(user=user)
        return render(request, 'auth/profile.html', {
            "user": user,
            "products": products
        })

class UpdateUser(View):
    def get(self, request, id):
        user = User.objects.get(id = id)
        return render(request, 'auth/update_profile.html', {"user": user})

    def post(self, request, id):
        user = get_object_or_404(User, id=id)

        user.username = request.POST.get('username')
        user.phone = request.POST.get('phone')
        balance_raw = request.POST.get('balance')
        if balance_raw:
            try:
                balance_cleaned = balance_raw.replace(',', '.')
                user.balance = Decimal(balance_cleaned)
            except (InvalidOperation, ValueError):
                pass


        user.save()
        return redirect('home')

class LogoutView(View):
    def get(self, request, id):
        user = User.objects.get(id=request.id)
        logout(user)
        return redirect('home')

class Recovery(View):
    def get(self, request):
        return render(request, 'auth/recovery_email.html')
    
    def post(self, request):
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'auth/recovery_email.html', {
                "error": "Bu emailga tegishli Foydalanuvchin topilmadi"
            })
        
        code = generate()

        Emailcode.objects.filter(users=user).delete()
        Emailcode.objects.filter(users=user, code=code)

        send_mail(
            subject="Parolni tiklash kodi",
            message=f"Sizning tasdiqlash kodingiz: {code}.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
        )
        request.session['recovery_email'] = email
        return redirect('recovery_code')

class ConfirmRecovery(View):
    def get(self, request):
        email = request.session.get('recovery_email', '')
        return render(request, 'auth/rec_code.html', {'email':email})
    
    def post(self, request):
        code = request.POST.get('code')
        email = request.session.get('recovery_email')

        if not email:
            return render(request, 'auth/rec_code.html', {
                "error": "Sessiya muddati tugagan"
            })
        try:
            emailobj = Emailcode.objects.get(users__email=email, code=code)
            if email.is_valid():
                user = emailobj.users
                user.is_active = True
                user.save

                emailobj.delete()
                return redirect('update_user', id= user.id)
            else:
                return render(request, 'auth/rec_code.html', {'error': 'Kodning amal qilish muddati tugagan'})
        except Emailcode.DoesNotExist:
            return render(request, 'auth/rec_code.html', {
                "error": "No`to`g`ri Kod Kiritildi"
            })