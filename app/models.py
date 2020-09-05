from django.db import models
import datetime
import uuid

from django.contrib.auth.models import User
# Create your models here.
from django.utils.html import format_html
from django.db.models import IntegerField, Model
from django.core.validators import MaxValueValidator, MinValueValidator
import random, os
from django.contrib.auth.models import AbstractUser
from django.db import models
# 安装 pip install django-multiselectfield
from multiselectfield import MultiSelectField

STATE_GENDER = ((0, "男"), (1, "女"), (2, "保密"))
ROLS_FRUIT = ((0, '西瓜'), (1, '草莓'), (2, '菠萝'))



# 大佬信息
class bossInfo(models.Model):
    name = models.CharField(verbose_name="姓名(文本类型)", max_length=225, null=False, blank=False, default="")
    # 课后练习 如何控制输入的 age 大于20 小于100
    age = models.IntegerField(verbose_name="年龄(数字类型)", null=False, blank=False, default=1)
    gender = models.IntegerField(verbose_name="性别(单选)", max_length=225, null=False, blank=False, default=1,
                              choices=STATE_GENDER)
    likeFruit = MultiSelectField(verbose_name="喜欢的水果(多选)", choices=ROLS_FRUIT)
    #headImage = models.ImageField(verbose_name="个人写真(图片文件)", null=False, blank=False, default=None)
    userUrl = models.URLField(verbose_name="个人主页(URL地址)", null=False, blank=False, default=None)
    desc = models.TextField(verbose_name="描述(多行文本)", max_length=1000, null=False, blank=False, default=None)
    # 通过model.  的提示在扩展8个字段  自由发挥
    createTime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    lastTime = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    creator = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="创建者",
                                related_name="bossinfo_creator")
    editor = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="修改者",
                               related_name="bossinfo_editor")

    class Meta:
        verbose_name = "大佬信息管理"
        verbose_name_plural = "大佬信息管理"

    def __str__(self):
        return self.name
