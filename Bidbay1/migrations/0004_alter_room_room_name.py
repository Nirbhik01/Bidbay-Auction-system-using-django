# Generated by Django 5.0.4 on 2024-08-21 10:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bidbay1', '0003_room_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='room_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bidbay1.items'),
        ),
    ]
