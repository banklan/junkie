# Generated by Django 3.1.2 on 2020-10-12 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20201009_0929'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='show_name',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='beneficiary',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='donation',
            name='comment',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
