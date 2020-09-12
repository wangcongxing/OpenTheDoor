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


# 角色表
class role(models.Model):
    name = models.CharField(verbose_name="角色", max_length=225, null=False, blank=False, default="")


class sports(models.Model):
    name = models.CharField(verbose_name="运动名称", max_length=225, null=False, blank=False, default="")


# 大佬信息
class bossInfo(models.Model):
    name = models.CharField(verbose_name="姓名(文本类型)", max_length=225, null=False, blank=False, default="")
    rls = models.ForeignKey(role, verbose_name="角色", null=True, blank=True, on_delete=models.SET_NULL, default=1)
    sports = models.ManyToManyField(sports, verbose_name="喜欢的运动",  blank=True,
                                    default=1)
    # 课后练习 如何控制输入的 age 大于20 小于100
    age = models.IntegerField(verbose_name="年龄(数字类型)", null=False, blank=False, default=1)
    gender = models.IntegerField(verbose_name="性别(单选)", null=False, blank=False, default=1,
                                 choices=STATE_GENDER)
    likeFruit = MultiSelectField(verbose_name="喜欢的水果(多选)", choices=ROLS_FRUIT)
    # headImage = models.ImageField(verbose_name="个人写真(图片文件)", null=False, blank=False, default=None)
    userUrl = models.URLField(verbose_name="个人主页(URL地址)", null=True, blank=True, default=None)
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


from django.db import models
import datetime
import uuid
from django.contrib.auth.models import User
# Create your models here.
from django.utils.html import format_html
from django.db.models import IntegerField, Model
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime
import random, os
from django.contrib.auth.models import AbstractUser
from django.db import models
import OpenTheDoor.settings as config

STATE_CHOICES = ((0, "是"), (1, "否"))
AUTHTYPE_CHOICES = ((1, '消息'), (2, 'EOA'), (3, '组织架构'))
DEVELOPMENTLANGUAGE_CHOICES = ((0, 'Python'), (1, 'Java'), (2, 'C#'), (3, 'GO'), (4, 'PHP'))


# 方法重命名
def rename(newname):
    def decorator(fn):
        fn.__name__ = newname
        return fn

    return decorator


def newImageName(instance, filename):
    filename = '{}.{}'.format(uuid.uuid4().hex, "png")
    return filename


# 生成预约订单号
# 用时间生成一个唯一随机数

def random_with_N_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return random.randint(range_start, range_end)


def get_ran_dom():
    nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
    randomNum = random_with_N_digits(3)  # 生成的随机整数n，其中0<=n<=100
    if randomNum <= 10:
        randomNum = str(0) + str(randomNum)
    uniqueNum = str(nowTime) + str(randomNum)
    return uniqueNum


# Create your models here.
# 实例化加解密对象

# 应用管理
class appManager(models.Model):
    name = models.CharField(verbose_name="应用名称", max_length=225, null=False, blank=False, default="")
    appid = models.CharField(verbose_name="应用Id", max_length=225, null=False, blank=False, default="")
    secret = models.CharField(verbose_name="应用秘钥", max_length=900, null=False, blank=False, default=None)
    authType = models.IntegerField(choices=AUTHTYPE_CHOICES, verbose_name="授权类型", null=False, blank=False, default=0)
    state = models.IntegerField(choices=STATE_CHOICES, verbose_name="是否禁用", null=False, blank=False, default=1)
    contactPerson = models.TextField(verbose_name="项目负责人", max_length=500, null=False, blank=False, default="")
    whitelist = models.TextField(verbose_name="IP白名单", max_length=500, null=False, blank=False, default="")
    domain = models.TextField(verbose_name="请求域名", max_length=500, null=False, blank=False, default="")

    createTime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    lastTime = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    creator = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="创建者",
                                related_name="appmanager_creator")
    editor = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="修改者",
                               related_name="appmanager_editor")

    class Meta:
        verbose_name = "应用管理"
        verbose_name_plural = "应用管理"

    def __str__(self):
        return self.name
