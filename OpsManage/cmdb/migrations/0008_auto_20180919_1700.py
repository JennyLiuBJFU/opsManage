# Generated by Django 2.1.1 on 2018-09-19 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0007_auto_20180914_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='cab_location',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='机柜位置'),
        ),
        migrations.AddField(
            model_name='asset',
            name='height',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='高度'),
        ),
    ]
