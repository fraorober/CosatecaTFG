# Generated by Django 4.1.1 on 2023-05-27 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CosatecaApp', '0005_rating_availability'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessengerService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sendDate', models.DateField()),
                ('body', models.CharField(max_length=1000)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CosatecaApp.person')),
            ],
        ),
    ]