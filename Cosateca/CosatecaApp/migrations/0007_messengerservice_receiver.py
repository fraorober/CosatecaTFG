# Generated by Django 4.2.1 on 2023-05-27 15:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CosatecaApp', '0006_messengerservice'),
    ]

    operations = [
        migrations.AddField(
            model_name='messengerservice',
            name='receiver',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='CosatecaApp.person'),
            preserve_default=False,
        ),
    ]