# Generated by Django 3.1.2 on 2021-02-19 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0033_auto_20210218_2133'),
    ]

    operations = [
        migrations.AddField(
            model_name='withdrawrequest',
            name='withdraw_type',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='passwordreset',
            name='token',
            field=models.CharField(default='e27e1cc3a473406f2b45fc887181e1a09c0383c6a5273d78bd9be6de533fefe55e72a23de7176408c4f2373cf42fc1e0da1c1f4a0986deeea4cc29b1e3f538af3f1519b977a3ce7e31d4939808b35b8c122386d249ae12a7', max_length=200),
        ),
    ]
