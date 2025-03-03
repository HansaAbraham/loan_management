from django.urls import path
from . import views  
from .views import login_user,verify_otp
from loginApp.views import login_user  


app_name = 'loginApp'  

urlpatterns = [
    path('', views.home_view, name='home'),
    path('signup-customer/', views.sign_up_view, name='signup'),
   path('login-customer/', views.login_user, name='login_customer'),

    path('logout-customer/', views.logout_view, name='logout_customer'),
    path('api/login/', login_user, name='login_user'),


    path('edit-customer/', views.edit_customer, name='edit_customer'),
    path('verify-otp/<int:user_id>/', verify_otp, name='verify_otp')
]











