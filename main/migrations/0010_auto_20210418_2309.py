# Generated by Django 3.1.7 on 2021-04-18 20:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='likes',
            name='account',
        ),
        migrations.AddField(
            model_name='likes',
            name='account',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='main.accounts'),
            preserve_default=False,
        ),
    ]
