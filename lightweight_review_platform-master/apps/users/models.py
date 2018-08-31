from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
# Create your models here.


class EmailVerifyRecord(models.Model):
    SEND_CHOICES = (
        ('register', u'注册'),
        ('forget', u'找回密码')
    )

    code = models.CharField(max_length=20, verbose_name=u'验证码')
    email = models.EmailField(max_length=50, verbose_name=u'邮箱')
    send_type = models.CharField(choices=SEND_CHOICES, max_length=10, verbose_name=u'邮件目的')
    send_time = models.DateTimeField(default=datetime.now, verbose_name=u'发送时间')

    class Meta:
        verbose_name = u'邮箱验证码'
        verbose_name_plural = verbose_name


class UserProfile(AbstractUser):

    GENDER_CHOICES = (
        ('male', '男'),
        ('female', '女'),
        ('secret', '保密'),
    )
    # 邮箱
    email = models.EmailField(unique=True, max_length=50, verbose_name=u'邮箱')
    # 昵称
    nickname = models.CharField(max_length=30, default=u'佚名大侠', verbose_name=u'昵称')
    # 性别
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='male', verbose_name=u'姓名')
    # 生日
    birthday = models.DateField(null=True, blank=True, verbose_name=u'生日')
    # 目前所在大学
    presentCollege = models.CharField(max_length=50, default=u'不愿透露', verbose_name=u'目前所在大学')
    # 目标大学
    targetCollege = models.CharField(max_length=50, default=u'还没想好', verbose_name=u'目标大学')
    # 头像
    avatar = models.ImageField(upload_to='image/%Y/%m', default=u'img/user.jpg')
    # 座右铭
    motto = models.CharField(max_length=100, default="这个童鞋很懒，竟然一句鸡汤都不留", verbose_name=u'座右铭')
    # 打卡天数
    checkin_days = models.PositiveIntegerField(default=0, verbose_name=u'打卡天数')
    # 上次打卡日期
    lastCheckinDate = models.DateField(null=True, blank=True, verbose_name=u'上次打卡日期')
    # 备忘录
    memo = models.TextField(max_length=200, default='', verbose_name=u'备忘录')

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
class Search(models.Model):
    """
    用户搜索内容
    """
    search_content=models.CharField(max_length=20,verbose_name=u'搜索内容')
    user_belong=models.ForeignKey(UserProfile, verbose_name=u'所属用户')
    class Meta:
        verbose_name = u'所属用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.search_content


class UserWeaknessCategory(models.Model):
    """
    弱项分类
    """
    name = models.CharField(max_length=10, verbose_name=u'弱项分类')
    user_belong = models.ForeignKey(UserProfile, verbose_name=u'所属用户')


    class Meta:
        verbose_name = u'弱项分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class UserWeaknessTag(models.Model):
    """
    弱项标签
    """
    name = models.CharField(max_length=20, default="", blank=True, null=True, verbose_name=u'弱项标签')
    score = models.IntegerField(default=1, verbose_name=u'弱项标签评分')  # 即该用户上传的题目中所含有该标签的次数
    category_belong = models.ForeignKey(UserWeaknessCategory, verbose_name=u'所属分类')

    class Meta:
        verbose_name = u'弱项标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name













