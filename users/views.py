from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import *

class Register(View):
    def get(self, request):
        return render(request, 'auth/register.html')
    
    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        profile = request.FILES.get('profile_image')
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
        if profile.endwidth()

        user = User.objects.create_user(
            username=username,
            
        )