from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('verify/', views.verify, name='verify'),
    path('logout/', views.logout_view, name='logout'),
]
