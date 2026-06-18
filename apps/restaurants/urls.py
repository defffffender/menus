from django.urls import path

from . import views

app_name = 'restaurants'

urlpatterns = [
    path('cabinet/', views.cabinet, name='cabinet'),
    path('cabinet/<str:slug>/', views.dashboard, name='dashboard'),
    path('cabinet/<str:slug>/tables/', views.tables, name='tables'),
    path('cabinet/<str:slug>/tables/<int:pk>/edit/', views.table_edit, name='table_edit'),
    path('cabinet/<str:slug>/tables/<int:pk>/delete/', views.table_delete, name='table_delete'),
    path('cabinet/<str:slug>/tables/<int:pk>/qr.png', views.table_qr_png, name='table_qr_png'),
    path('cabinet/<str:slug>/qr/', views.qr_sheet, name='qr_sheet'),
    path('cabinet/<str:slug>/staff/', views.staff, name='staff'),
    path('cabinet/<str:slug>/staff/<int:pk>/role/', views.staff_role, name='staff_role'),
    path('cabinet/<str:slug>/staff/<int:pk>/remove/', views.staff_remove, name='staff_remove'),
    # публичное меню стола (по QR)
    path('m/<str:qr_token>/', views.guest_menu, name='guest_menu'),
]
