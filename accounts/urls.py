from django.urls import path
from .import views

urlpatterns = [
    
    path('register', views.register,name='register'),
    path('login', views.login,name='login'),
    path('logout/', views.logout,name='logout'),
    path('activate/<uidb64>/<token>',views.activate,name = 'activate'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('forgotpassword/',views.forgotpassword,name='forgotpassword'),
    path('resetpassword_validate/<uidb64>/<token>/',views.resetpassword_validate,name = 'resetpassword_validate'),
    path('verify_code/', views.verify_code,name='verify_code'),
    path('phone_verify/', views.phone_verify,name='phone_verify'),
    # path('forgotPassword_otp/', views.forgotPassword_otp,name='forgotPassword_otp'),
    # path('resetPassword/', views.resetPassword,name='resetPassword'),
]