# Generated by Django 4.1.1 on 2023-06-02 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CosatecaApp', '0023_alter_product_image_alter_rating_rating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='date',
            new_name='create_date',
        ),
        migrations.AddField(
            model_name='rating',
            name='subject',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='rating',
            name='update_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
