# Generated by Django 3.1.2 on 2020-12-03 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0027_auto_20201203_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordreset',
            name='token',
            field=models.CharField(default='c7a5d209dcadf05558d21281d6ff8300132853899398ca95c58118708f5ac3a73118a51ecda069a355f3b599cb2f0f783b3639f0dfe4291d64542c9345bf6dc767894d4a78a84ea76959947e122a5fc060497c99e31e7984', max_length=200),
        ),
    ]
