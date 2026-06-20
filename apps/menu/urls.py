from django.urls import path

from . import views

app_name = 'menu'

urlpatterns = [
    path('cabinet/<str:slug>/menu/', views.menu, name='menu'),

    path('cabinet/<str:slug>/menu/categories/', views.category_add, name='category_add'),
    path('cabinet/<str:slug>/menu/categories/reorder/', views.category_reorder, name='category_reorder'),
    path('cabinet/<str:slug>/menu/categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('cabinet/<str:slug>/menu/categories/<int:pk>/delete/', views.category_delete, name='category_delete'),

    path('cabinet/<str:slug>/menu/dishes/new/', views.dish_add, name='dish_add'),
    path('cabinet/<str:slug>/menu/dishes/reorder/', views.dish_reorder, name='dish_reorder'),
    path('cabinet/<str:slug>/menu/dishes/<int:pk>/edit/', views.dish_edit, name='dish_edit'),
    path('cabinet/<str:slug>/menu/dishes/<int:pk>/delete/', views.dish_delete, name='dish_delete'),
    path('cabinet/<str:slug>/menu/dishes/<int:pk>/toggle/', views.dish_toggle, name='dish_toggle'),
]
