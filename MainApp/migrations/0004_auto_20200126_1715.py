# Generated by Django 2.2.6 on 2020-01-26 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0003_auto_20200126_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='camera_one_image',
            name='down_date',
            field=models.CharField(default='19 10 1997', max_length=100),
        ),
        migrations.AddField(
            model_name='camera_two_image',
            name='down_date',
            field=models.CharField(default='19 10 1997', max_length=100),
        ),
    ]
