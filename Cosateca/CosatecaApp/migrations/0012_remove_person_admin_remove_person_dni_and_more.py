# Generated by Django 4.2.1 on 2023-05-29 10:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CosatecaApp', '0011_remove_person_usuario_person_admin_person_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='admin',
        ),
        migrations.RemoveField(
            model_name='person',
            name='dni',
        ),
        migrations.RemoveField(
            model_name='person',
            name='email',
        ),
        migrations.RemoveField(
            model_name='person',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='person',
            name='password',
        ),
        migrations.RemoveField(
            model_name='person',
            name='username',
        ),
    ]