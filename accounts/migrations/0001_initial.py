# Generated by Django 4.0.6 on 2022-07-21 15:43

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', migrations.swappable_dependency(settings.AUTH_USER_MODEL)),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(max_length=100, unique=True)),
                ('permissions', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=10, null=True), size=8)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, auto_now=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(error_messages={'unique': 'A user with that email already exists.'}, max_length=255, unique=True, verbose_name='email address')),
                ('is_email_verified', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_user', models.BooleanField(default=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('contact', models.BigIntegerField(blank=True, null=True)),
                ('is_contact_verified', models.BooleanField(default=False)),
                ('company_name', models.CharField(blank=True, max_length=300, null=True)),
                ('logo', models.CharField(blank=True, max_length=300, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('roles', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.role')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
