from django.urls import path
from .views import *

from django.contrib.auth.decorators import login_required

app_name = 'customer'
urlpatterns = [
    path('',trang_chu, name='trang_chu'),
    path('views',view_realtime, name='views'),
    path('view_data',view_data, name='view_data'),
    
    ]