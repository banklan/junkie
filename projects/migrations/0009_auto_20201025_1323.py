# Generated by Django 3.1.2 on 2020-10-25 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_auto_20201025_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='expiry',
            field=models.DateTimeField(),
        ),
    ]
