# Generated by Django 2.1.1 on 2018-09-14 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0006_auto_20180914_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cabinetspace',
            name='cabinet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cmdb.Cabinet', verbose_name='所在机柜'),
        ),
    ]
