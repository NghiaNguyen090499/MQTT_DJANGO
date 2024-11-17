from django.db import models

class DeviceStatus(models.Model):
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    speed = models.FloatField(null=True, blank=True)
    up_down_count = models.IntegerField(default=0)
    down_up_count = models.IntegerField(default=0)
    total_gb = models.FloatField(default=0)
    used_gb = models.FloatField(default=0)
    free_gb = models.FloatField(default=0)
    usage_percent = models.FloatField(default=0)
    storage_full = models.BooleanField(default=False)
    temperature = models.FloatField(default=0)
    gps_status = models.CharField(max_length=50, default='Unknown')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        
    def __str__(self):
        return f"Device Status at {self.timestamp}"
    
    
    
class PhuHuynh(models.Model):
    ho_va_ten = models.CharField(max_length=200,null=True)
    thanh_toan = models.BooleanField(default=0)
 
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ho_va_ten {self.ho_va_ten}"