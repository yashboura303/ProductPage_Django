# Generated by Django 2.2.5 on 2019-11-08 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productsHome', '0003_auto_20191108_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='image',
            field=models.ImageField(upload_to='productImages/'),
        ),
    ]
