import os
import django
import paho.mqtt.client as mqtt
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import logging
# Thiết lập môi trường Django
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ARAR_COUNTING.settings')
django.setup()

# Thiết lập logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cấu hình MQTT Broker và topic
MQTT_BROKER = "18.117.130.119"
MQTT_PORT = 1883
MQTT_TOPIC = "maixcam/data"

# Hàm callback khi kết nối thành công đến MQTT Broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Đã kết nối thành công tới MQTT Broker")
        client.subscribe(MQTT_TOPIC)
        logger.info(f"Đã đăng ký topic: {MQTT_TOPIC}")
    else:
        logger.error(f"Kết nối thất bại, mã lỗi {rc}")

# Hàm callback khi nhận được tin nhắn từ MQTT Broker
def on_message(client, userdata, message):
    try:
        data = message.payload.decode()
        logger.info(f"Nhận dữ liệu từ {message.topic}: {data}")

        # Gửi dữ liệu đến WebSocket group
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "realtime_data",  # Tên nhóm WebSocket
            {
                "type": "send_realtime_data",
                "message": data,
            },
        )
        logger.info("Đã gửi dữ liệu tới WebSocket group 'realtime_data'")
    except Exception as e:
        logger.error(f"Lỗi khi gửi dữ liệu tới WebSocket: {e}")

# Thiết lập MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    logger.info("Đang kết nối MQTT client...")
    client.loop_start()
except Exception as e:
    logger.error(f"Lỗi kết nối MQTT: {e}")

# Giữ cho script chạy liên tục
try:
    while True:
        pass
except KeyboardInterrupt:
    logger.info("Đang ngắt kết nối từ MQTT Broker...")
    client.loop_stop()
    client.disconnect()
    logger.info("Đã ngắt kết nối thành công.")
