from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
import ast

# Biến lưu trữ dữ liệu POST đầu tiên
stored_data = {}

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
import time
from counting_bus.models import DeviceStatus, PhuHuynh

# Biến lưu trữ dữ liệu và thời gian xử lý gần nhất
stored_data = {}
last_processed_time = 0
TIME_THRESHOLD = 1  # Giới hạn xử lý mỗi giây

@csrf_exempt
def trang_chu(request):
    global stored_data, last_processed_time
    
    if request.method == 'POST':
        current_time = time.time()

        # Chỉ xử lý nếu đã qua khoảng thời gian cho phép
        if current_time - last_processed_time > TIME_THRESHOLD:
            try:
                # Giải mã dữ liệu JSON từ request body
                received_data = json.loads(request.body)
                print(f"Data received: {received_data}")

                # Kiểm tra dữ liệu mới khác với dữ liệu cũ
                if received_data != stored_data:
                    # Cập nhật dữ liệu và thời gian xử lý
                    stored_data = {k: (v if v is not None else "N/A") for k, v in received_data.items()}
                    last_processed_time = current_time
                    print(f"Processed data: {stored_data}")

            except json.JSONDecodeError:
                stored_data = {"error": "Dữ liệu không hợp lệ"}
        
    # Trả dữ liệu hiện tại cho template
    return render(request, 'counting.html', {'data': stored_data})





def view_realtime(request):
    return render(request, 'count_realtime.html')


def view_data(request):
    data = DeviceStatus.objects.filter(gps_status='OK')[:9]
    print('ok')
    phu_huynh = PhuHuynh.objects.filter(thanh_toan=0)
    return render(request, 'view_data.html',{'data':data,'phu_huynh':phu_huynh}) 