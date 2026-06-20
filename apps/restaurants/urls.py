from django.urls import path

from . import views

app_name = 'restaurants'

urlpatterns = [
    path('cabinet/', views.cabinet, name='cabinet'),
    path('cabinet/new/', views.venue_create, name='venue_create'),
    path('cabinet/<str:slug>/', views.dashboard, name='dashboard'),
    path('cabinet/<str:slug>/tables/', views.tables, name='tables'),
    path('cabinet/<str:slug>/tables/<int:pk>/edit/', views.table_edit, name='table_edit'),
    path('cabinet/<str:slug>/tables/<int:pk>/delete/', views.table_delete, name='table_delete'),
    path('cabinet/<str:slug>/tables/<int:pk>/waiters/', views.table_waiters, name='table_waiters'),
    path('cabinet/<str:slug>/tables/reorder/', views.table_reorder, name='table_reorder'),
    path('cabinet/<str:slug>/zones/add/', views.zone_add, name='zone_add'),
    path('cabinet/<str:slug>/zones/reorder/', views.zone_reorder, name='zone_reorder'),
    path('cabinet/<str:slug>/zones/<int:pk>/edit/', views.zone_edit, name='zone_edit'),
    path('cabinet/<str:slug>/zones/<int:pk>/delete/', views.zone_delete, name='zone_delete'),
    path('cabinet/<str:slug>/tables/<int:pk>/qr.png', views.table_qr_png, name='table_qr_png'),
    path('cabinet/<str:slug>/qr/', views.qr_sheet, name='qr_sheet'),
    path('cabinet/<str:slug>/analytics/', views.analytics, name='analytics'),
    path('cabinet/<str:slug>/settings/', views.settings_view, name='settings'),
    path('cabinet/<str:slug>/design/', views.menu_design, name='menu_design'),
    path('cabinet/<str:slug>/design/preview/', views.menu_design_preview, name='menu_design_preview'),
    path('cabinet/<str:slug>/staff/', views.staff, name='staff'),
    path('cabinet/<str:slug>/staff/<int:pk>/role/', views.staff_role, name='staff_role'),
    path('cabinet/<str:slug>/staff/<int:pk>/remove/', views.staff_remove, name='staff_remove'),
    # публичное меню стола (по QR)
    path('m/<str:qr_token>/', views.guest_menu, name='guest_menu'),
]
