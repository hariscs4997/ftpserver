# Generated by Django 2.2.6 on 2020-01-26 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0004_auto_20200126_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statemodel',
            name='camera_one',
            field=models.CharField(default='empty', max_length=200),
        ),
        migrations.AlterField(
            model_name='statemodel',
            name='camera_two',
            field=models.CharField(default='empty', max_length=200),
        ),
    ]