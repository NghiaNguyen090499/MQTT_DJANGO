# Generated by Django 5.1.2 on 2024-11-07 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField(default=0.0)),
                ('longitude', models.FloatField(default=0.0)),
                ('speed', models.FloatField(blank=True, null=True)),
                ('up_down_count', models.IntegerField(default=0)),
                ('down_up_count', models.IntegerField(default=0)),
                ('total_gb', models.FloatField(default=0)),
                ('used_gb', models.FloatField(default=0)),
                ('free_gb', models.FloatField(default=0)),
                ('usage_percent', models.FloatField(default=0)),
                ('storage_full', models.BooleanField(default=False)),
                ('temperature', models.FloatField(default=0)),
                ('gps_status', models.CharField(default='Unknown', max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
