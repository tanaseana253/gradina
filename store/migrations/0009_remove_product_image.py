# Generated by Django 5.0.6 on 2024-06-27 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_product_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
    ]
