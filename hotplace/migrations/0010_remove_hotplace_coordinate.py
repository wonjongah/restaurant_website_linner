# Generated by Django 3.1 on 2020-08-20 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotplace', '0009_auto_20200820_1211'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotplace',
            name='coordinate',
        ),
    ]