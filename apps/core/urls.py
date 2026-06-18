from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.LandingView.as_view(), name='landing'),
    path('i18n/set/', views.set_language, name='set_language'),
]
