# Generated by Django 3.1.2 on 2020-10-25 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_auto_20201025_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
