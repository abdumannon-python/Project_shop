from django.urls import path
from .views import *

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify/', VerifyPage.as_view(), name='verify'),
    path('updateuser/<int:id>/', UpdateUser.as_view(), name='updata_user'),
    path('profile/<int:id>/', Profile.as_view(), name='profile'),
    path('recovery/', Recovery.as_view(), name='recovery'),
    path('confirmrecovery/', ConfirmRecovery.as_view(), name='confirm_recovery')
    
]