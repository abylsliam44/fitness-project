# Generated by Django 5.1.6 on 2025-04-07 20:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0008_product_address_product_city_product_latitude_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='address',
        ),
        migrations.RemoveField(
            model_name='product',
            name='city',
        ),
        migrations.RemoveField(
            model_name='product',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='product',
            name='longitude',
        ),
    ]
