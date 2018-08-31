from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from users.models import UserProfile
# Create your models here.

class Tag(models.Model):
    """
    标签
    """

    name = models.CharField(max_length=20, verbose_name=u'错题标签', default="", blank=True, null=True)
    score = models.IntegerField(default=1, verbose_name=u'错题标签的评分')

    class Meta:
        verbose_name = "错题标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Question(models.Model):
    """
    题目收集
    """
    CATEGORY_CHOICE = (
        (u'math', u'数学'),
        (u'english', u'英语'),
        (u'politic', u'政治'),
        (u'major', u'专业课'),
    )

    title = RichTextUploadingField(max_length=1000, null=False, verbose_name=u'题目')
    tags = models.ManyToManyField(Tag, verbose_name=u'标签')
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICE, verbose_name=u'分类')
    answer = RichTextUploadingField(max_length=1000, default='', verbose_name=u'答案')
    note = RichTextUploadingField(max_length=1000, default='', verbose_name=u'笔记')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    modified_time = models.DateTimeField(auto_now=True, verbose_name=u'最后修改时间')

    user_belong = models.ForeignKey(UserProfile, verbose_name=u'所属用户')

    class Meta:
        verbose_name = u'错题整理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Hotspot(models.Model):
    """
    时事热点
    """
    title = models.CharField(max_length=100, null=False, blank=False, verbose_name=u'标题')
    content = models.TextField(verbose_name=u'正文')
    date = models.DateField(auto_now=True, verbose_name=u'添加日期')

    class Meta:
        verbose_name = u'时事热点'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class CommonWeaknessCategory(models.Model):
    """
    公共弱点分类
    """
    name = models.CharField(max_length=10, unique=True, verbose_name=u'弱项分类')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'公共弱项分类'
        verbose_name_plural = verbose_name


class CommonWeaknessTag(models.Model):
    """
    公共弱点标签
    """
    name = models.CharField(max_length=20, unique=True, default="", blank=True, null=True, verbose_name=u'弱项标签')
    category_belong = models.ForeignKey(CommonWeaknessCategory, verbose_name=u'所属分类')

    class Meta:
        verbose_name = u'公共弱项标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name











