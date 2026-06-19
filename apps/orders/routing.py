from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/cabinet/<str:slug>/orders/', consumers.CabinetOrdersConsumer.as_asgi()),
    path('ws/o/<str:token>/', consumers.GuestOrderConsumer.as_asgi()),
]
