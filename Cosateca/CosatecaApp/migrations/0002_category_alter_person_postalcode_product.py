# Generated by Django 4.2.1 on 2023-05-27 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CosatecaApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='person',
            name='postalCode',
            field=models.CharField(max_length=5),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('barcode', models.CharField(max_length=12)),
                ('image', models.ImageField(upload_to='')),
                ('description', models.CharField(max_length=500)),
                ('publicationDate', models.DateField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CosatecaApp.category')),
            ],
        ),
    ]