# Generated by Django 3.1 on 2020-08-25 09:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='bossInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=225, verbose_name='姓名(文本类型)')),
                ('age', models.IntegerField(default=1, verbose_name='年龄(数字类型)')),
                ('gender', models.CharField(choices=[(0, '男'), (1, '女'), (2, '保密')], default=1, max_length=225, verbose_name='性别(单选)')),
                ('likeFruit', multiselectfield.db.fields.MultiSelectField(choices=[(0, '西瓜'), (1, '草莓'), (2, '菠萝')], max_length=5, verbose_name='喜欢的水果(多选)')),
                ('userUrl', models.URLField(default=None, verbose_name='个人主页(URL地址)')),
                ('desc', models.TextField(default=None, max_length=1000, verbose_name='描述(多行文本)')),
                ('createTime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('lastTime', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bossinfo_creator', to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
                ('editor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bossinfo_editor', to=settings.AUTH_USER_MODEL, verbose_name='修改者')),
            ],
            options={
                'verbose_name': '大佬信息管理',
                'verbose_name_plural': '大佬信息管理',
            },
        ),
    ]
