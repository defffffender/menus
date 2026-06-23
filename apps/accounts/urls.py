from django.urls import path

from . import agent_views, views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),  # теперь форма «Оставить заявку»
    path('login/', views.login_view, name='login'),
    path('verify/', views.verify, name='verify'),
    path('verify/resend/', views.resend, name='resend'),
    path('password/reset/', views.password_reset, name='password_reset'),
    path('password/new/', views.password_reset_set, name='password_reset_set'),
    path('logout/', views.logout_view, name='logout'),

    # агентский кабинет
    path('agent/', agent_views.dashboard, name='agent_dashboard'),
    path('agent/new/', agent_views.register_venue, name='agent_register_venue'),
    path('agent/<int:pk>/password/', agent_views.reset_password, name='agent_reset_password'),
]
