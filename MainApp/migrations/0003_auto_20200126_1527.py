# Generated by Django 2.2.6 on 2020-01-26 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0002_statemodel_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='camera_one_image',
            name='down_time',
            field=models.CharField(default='19 10 1997 05:35', max_length=100),
        ),
        migrations.AddField(
            model_name='camera_two_image',
            name='down_time',
            field=models.CharField(default='19 10 1997 05:35', max_length=100),
        ),
    ]