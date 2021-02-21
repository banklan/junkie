# Generated by Django 3.1.2 on 2020-12-04 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0028_auto_20201203_2136'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='passwordreset',
            name='token',
            field=models.CharField(default='2dfc03e5f228e3ff29d7ae305da5be71001799bff095e738f7c33dcc6df018f61d6c9181b09dda58d3ae5c62c84e12a2abc00ba2b4795e4c54dd63e19dd15161241b2796a70dc8b959298007a19042b6b21bdab66fbed0a4', max_length=200),
        ),
    ]
