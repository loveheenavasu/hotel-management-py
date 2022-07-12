# Generated by Django 4.0.6 on 2022-07-12 14:50

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_alter_role_permission'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='role',
            name='permission',
        ),
        migrations.AddField(
            model_name='role',
            name='permissions',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=10, null=True), default=None, size=8),
            preserve_default=False,
        ),
    ]
