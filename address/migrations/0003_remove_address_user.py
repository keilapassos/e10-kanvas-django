# Generated by Django 4.0.3 on 2022-03-19 23:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='user',
        ),
    ]
