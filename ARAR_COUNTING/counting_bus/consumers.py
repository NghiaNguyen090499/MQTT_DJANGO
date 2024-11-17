import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ARAR_COUNTING.settings')

# Đảm bảo django.setup() được gọi trước khi import models
import django
django.setup()

import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from counting_bus.models import DeviceStatus

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class RealtimeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("realtime_data", self.channel_name)
        await self.accept()
        logger.info("WebSocket connection established.")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("realtime_data", self.channel_name)
        logger.info("WebSocket connection closed.")

    async def send_realtime_data(self, event):
        message = event["message"]
        logger.info(f"Received message from channel layer: {message}")
        
        # Lưu dữ liệu vào database
        try:
            await self.save_device_status(message)
            logger.info("Successfully saved device status to database")
        except Exception as e:
            logger.error(f"Error saving to database: {str(e)}")
        
        # Gửi dữ liệu đến WebSocket client
        await self.send(text_data=json.dumps({"message": message}))
        logger.info(f"Message sent to WebSocket client: {message}")

    @database_sync_to_async
    def save_device_status(self, message):
        try:
            # Chuyển đổi message thành dict nếu nó là string
            data = json.loads(message) if isinstance(message, str) else message
            print(data)
            # Tạo bản ghi mới trong database
            DeviceStatus.objects.create(
                latitude=data.get('latitude', 0.0),
                longitude=data.get('longitude', 0.0),
                speed=data.get('speed'),
                up_down_count=data.get('up_down_count', 0),
                down_up_count=data.get('down_up_count', 0),
                total_gb=data.get('total_gb', 0),
                used_gb=data.get('used_gb', 0),
                free_gb=data.get('free_gb', 0),
                usage_percent=data.get('usage_percent', 0),
                storage_full=data.get('storage_full', False),
                temperature=data.get('temperature', 0),
                gps_status=data.get('gps_status', 'Unknown'),
                timestamp=timezone.now()
            )
            
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON message: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error creating database record: {str(e)}")
            raise