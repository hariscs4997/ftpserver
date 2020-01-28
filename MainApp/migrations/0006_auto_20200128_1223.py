# Generated by Django 2.2.6 on 2020-01-28 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0005_auto_20200127_0006'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='camera_one_image',
            name='image',
        ),
        migrations.RemoveField(
            model_name='camera_two_image',
            name='image',
        ),
        migrations.AddField(
            model_name='camera_one_image',
            name='image_url',
            field=models.CharField(default='https://i.picsum.photos/id/113/536/354.jpg', max_length=1000),
        ),
        migrations.AddField(
            model_name='camera_two_image',
            name='image_url',
            field=models.CharField(default='https://i.picsum.photos/id/113/536/354.jpg', max_length=1000),
        ),
    ]
