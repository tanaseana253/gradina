# Generated by Django 5.0.6 on 2024-06-27 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_remove_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='static/images'),
        ),
    ]
