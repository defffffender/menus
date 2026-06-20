from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('verify/', views.verify, name='verify'),
    path('verify/resend/', views.resend, name='resend'),
    path('password/reset/', views.password_reset, name='password_reset'),
    path('password/new/', views.password_reset_set, name='password_reset_set'),
    path('logout/', views.logout_view, name='logout'),
]
