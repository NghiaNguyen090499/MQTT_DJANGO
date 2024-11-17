import paho.mqtt.client as mqtt
import json
import requests

# Cấu hình MQTT Broker và topic
MQTT_BROKER = "18.117.130.119"
MQTT_PORT = 1883
MQTT_TOPIC = "maixcam/data"  # Đặt topic MaixCam đang gửi dữ liệu lên

# URL Django để gửi dữ liệu
DJANGO_URL = "http://127.0.0.1:8000/"  # Thay bằng URL thực tế của bạn

# Hàm callback khi kết nối MQTT thành công
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")
        client.subscribe(MQTT_TOPIC)
    else:
        print("Failed to connect, return code %d\n", rc)

# Hàm callback khi nhận được tin nhắn từ MQTT
def on_message(client, userdata, message):
    data = message.payload.decode()
    print(f"Received data from {message.topic}: {data}")

    # Chuyển đổi dữ liệu thành JSON (nếu cần)
    try:
        json_data = json.loads(data)  # Giả sử dữ liệu là JSON
    except json.JSONDecodeError:
        json_data = {"message": data}  # Nếu không phải JSON, gói vào từ điển

    # Gửi dữ liệu đến URL Django bằng POST request
    try:
        response = requests.post(DJANGO_URL, json=json_data)
        if response.status_code == 200:
            print("Data posted to Django successfully")
        else:
            print(f"Failed to post data, status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error posting data: {e}")

# Thiết lập MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Kết nối tới MQTT Broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Bắt đầu vòng lặp để nhận dữ liệu
client.loop_forever()
