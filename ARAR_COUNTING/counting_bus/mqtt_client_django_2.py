import paho.mqtt.client as mqtt
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Cấu hình MQTT Broker và topic
MQTT_BROKER = "18.117.130.119"
MQTT_PORT = 1883
MQTT_TOPIC = "maixcam/data"  # Đặt topic MaixCam đang gửi dữ liệu lên

# Hàm callback khi kết nối MQTT thành công
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker")
    client.subscribe(MQTT_TOPIC)

# Hàm callback khi nhận được tin nhắn từ MQTT
def on_message(client, userdata, message):
    data = message.payload.decode()
    print(f"Received data from {message.topic}: {data}")
    
    # Gửi dữ liệu tới WebSocket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "realtime_data",  # Tên nhóm WebSocket
        {
            "type": "send_realtime_data",
            "message": data,
        },
    )

# Thiết lập MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()
