# Generated by Django 4.0.6 on 2022-07-18 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_imageupload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageupload',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]