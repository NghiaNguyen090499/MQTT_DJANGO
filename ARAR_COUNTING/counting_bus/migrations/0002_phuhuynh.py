# Generated by Django 5.1.2 on 2024-11-07 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counting_bus', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhuHuynh',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ho_va_ten', models.CharField(max_length=200, null=True)),
                ('thanh_toan', models.BooleanField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]