# Generated by Django 4.2.2 on 2023-06-21 19:06

import CosatecaApp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CosatecaApp', '0006_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('SPORTS', 'Sports'), ('MACHINERY', 'Machinery'), ('TOOLS', 'Tools'), ('GARDENING', 'Gardening'), ('VIDEOGAMES', 'Videogames'), ('CONSOLES', 'Consoles'), ('BOOKS', 'Books'), ('PCs', 'Pcs'), ('TABLETS', 'Tablets'), ('MOBILE PHONE', 'Mobile Phone'), ('ART', 'Art'), ('PHOTOGRAPHY', 'Photography'), ('KITCHEN', 'Kitchen'), ('INSTRUMENTS', 'Instruments')], max_length=12, verbose_name=CosatecaApp.models.Category),
        ),
        migrations.AlterField(
            model_name='report',
            name='reason',
            field=models.CharField(choices=[('FRAUDULENT BEHAVIOR', 'Fraudulent Behavior'), ('DAMAGE OR LOSS OBJECTS', 'Damage Or Loss Objects'), ('ILLEGAL ACTIVITIES', 'Illegal Activities')], max_length=25, verbose_name=CosatecaApp.models.Reason),
        ),
    ]
