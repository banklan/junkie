# Generated by Django 3.1.2 on 2021-02-25 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0036_auto_20210221_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordreset',
            name='token',
            field=models.CharField(default='d980d80033010ac27694f3e4318c9969b7cc3cbfeadd6d5c443c8cf124054f6562bd5b1a9204bb2dfc9aa7513fd854175b65d415963a72741a07315834da7ac30980eae4bac5c16a893bac2fa8a24dee83809904f77657f1', max_length=200),
        ),
    ]
