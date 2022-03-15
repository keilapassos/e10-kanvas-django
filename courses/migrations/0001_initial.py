# Generated by Django 4.0.3 on 2022-03-15 12:01

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('demo_time', models.TimeField()),
                ('created_at', models.DateTimeField()),
                ('link_repo', models.TextField()),
            ],
        ),
    ]
