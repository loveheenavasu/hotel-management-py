# Generated by Django 4.0.6 on 2022-07-13 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_alter_menucategory_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='role_name',
            field=models.CharField(default=None, max_length=100, unique=True),
            preserve_default=False,
        ),
    ]
