# Generated by Django 3.1 on 2020-09-05 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20200905_0856'),
    ]

    operations = [
        migrations.CreateModel(
            name='commodity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=225, verbose_name='商品名称')),
                ('desc', models.TextField(blank=True, verbose_name='商品描述')),
            ],
            options={
                'verbose_name_plural': '商品表',
            },
        ),
    ]
