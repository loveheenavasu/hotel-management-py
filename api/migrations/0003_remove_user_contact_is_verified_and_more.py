# Generated by Django 4.0.5 on 2022-07-04 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_role_permission_alter_role_role_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='contact_is_verified',
        ),
        migrations.AddField(
            model_name='user',
            name='is_contact_verified',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='contact',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
