# Generated by Django 2.2.5 on 2019-11-08 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productsHome', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='image',
            field=models.ImageField(height_field=400, upload_to='productImages/', width_field=400),
        ),
    ]
