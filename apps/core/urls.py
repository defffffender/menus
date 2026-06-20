from django.urls import path

from . import admin_views, views

app_name = 'core'

urlpatterns = [
    path('', views.LandingView.as_view(), name='landing'),
    path('i18n/set/', views.set_language, name='set_language'),
    # данные для платформенного дашборда в /admin (только для staff)
    path('manage/dashboard-data/', admin_views.admin_dashboard_data, name='admin_dashboard_data'),
]
