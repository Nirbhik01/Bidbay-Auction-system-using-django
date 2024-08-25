# Generated by Django 5.0.4 on 2024-08-21 09:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bidbay1', '0002_remove_items_item_current_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('room_id', models.AutoField(primary_key=True, serialize=False)),
                ('room_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=500)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Bidbay1.userdetails')),
                ('room_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bidbay1.room')),
            ],
        ),
    ]