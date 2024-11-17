from django.urls import re_path,path
from . import consumers

websocket_urlpatterns = [
    path('ws/realtime_data/', consumers.RealtimeConsumer.as_asgi()),
]
