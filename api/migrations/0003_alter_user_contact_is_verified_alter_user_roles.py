# Generated by Django 4.0.6 on 2022-07-06 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_user_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='contact_is_verified',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='roles',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.role'),
        ),
    ]
