# Generated by Django 4.2.2 on 2023-06-22 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CosatecaApp', '0010_report_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='capture',
            field=models.ImageField(blank=True, null=True, upload_to='reports'),
        ),
    ]
