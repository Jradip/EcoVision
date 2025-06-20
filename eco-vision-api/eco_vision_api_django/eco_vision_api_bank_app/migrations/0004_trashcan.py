# Generated by Django 5.2.1 on 2025-06-09 15:02

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eco_vision_api_bank_app', '0003_alter_openinghour_id_alter_wastebank_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrashCan',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('accepted_waste_types', models.ManyToManyField(to='eco_vision_api_bank_app.wastetype')),
            ],
        ),
    ]
