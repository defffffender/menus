from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    # гость
    path('m/<str:qr_token>/order/', views.create_order, name='create'),
    path('o/<str:token>/', views.order_status, name='status'),
    path('o/<str:token>/poll/', views.order_status_poll, name='status_poll'),

    # кабинет
    path('cabinet/<str:slug>/orders/', views.orders, name='orders'),
    path('cabinet/<str:slug>/orders/history/', views.orders_history, name='history'),
    path('cabinet/<str:slug>/orders/feed/', views.orders_feed, name='feed'),
    path('cabinet/<str:slug>/orders/<int:pk>/status/', views.order_set_status, name='set_status'),
    path('cabinet/<str:slug>/tables/<int:table_pk>/close/', views.close_table, name='close_table'),
]
