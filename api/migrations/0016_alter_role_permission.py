# Generated by Django 4.0.6 on 2022-07-12 11:56

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_alter_role_permission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='permission',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, size=10),
        ),
    ]
