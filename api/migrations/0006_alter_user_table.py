# Generated by Django 4.0.6 on 2022-07-06 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_user_options_alter_user_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='user',
            table='user',
        ),
    ]