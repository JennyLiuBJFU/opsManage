# Generated by Django 2.1.1 on 2018-09-13 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0003_auto_20180910_1228'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='qrcode',
            field=models.URLField(blank=True, null=True, verbose_name='二维码'),
        ),
        migrations.AlterField(
            model_name='disk',
            name='disk_status',
            field=models.CharField(blank=True, choices=[('1', '正常'), ('2', '故障'), ('3', '下线')], max_length=100, null=True),
        ),
    ]
