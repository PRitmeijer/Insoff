# Generated by Django 4.0 on 2022-11-20 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charts', '0003_rename_asset_pricestat_asset_pricestat_count_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='api_name',
            field=models.CharField(default='', max_length=30, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='asset',
            name='provider',
            field=models.IntegerField(choices=[(0, 'KRAKEN')], default=0),
        ),
    ]
