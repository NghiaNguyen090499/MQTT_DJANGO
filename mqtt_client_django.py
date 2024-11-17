# run_mqtt_client.py
import os
import django
from django.conf import settings

# Đặt DJANGO_SETTINGS_MODULE trước khi thiết lập Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ARAR_COUNTING.settings")
django.setup()

import paho.mqtt.client as mqtt
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

MQTT_BROKER = "18.117.130.119"
MQTT_PORT = 1883
MQTT_TOPIC = "maixcam/data"

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, message):
    data = message.payload.decode()
    print(f"Received data from {message.topic}: {data}")
    
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "realtime_data",
        {
            "type": "send_realtime_data",
            "message": data,
        },
    )

def run_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    print("Starting MQTT client...")
    client.loop_forever()

if __name__ == "__main__":
    run_mqtt_client()