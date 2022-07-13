# Generated by Django 4.0.6 on 2022-07-12 19:06

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_remove_role_created_at_remove_role_permissions_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='role',
            name='permissions',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=10, null=True), default=None, size=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='role',
            name='role_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='role',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]