# Generated by Django 2.1.1 on 2018-11-09 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventlog',
            name='event_type',
            field=models.CharField(choices=[('1', '增加'), ('2', '删除'), ('3', '修改')], max_length=128, verbose_name='事件类型'),
        ),
    ]