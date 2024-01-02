from django.db import models

# 管理员表
class AdminUser(models.Model):
    name = models.CharField('用户名', max_length=128)
    password = models.CharField('密码', max_length=256)

    class Meta:
        verbose_name = '管理员'
        verbose_name_plural = '管理员'

    def __str__(self):
        return self.name

#角色表:台领导、中层干部、普通职工
class Grade(models.Model):

    grade = models.CharField('角色',max_length=20)
    weight = models.FloatField('角色权重',default=1)

    class Meta:
        verbose_name = '角色'
        verbose_name_plural = '角色'

    def __str__(self):
        return self.grade

#部门表
class Department(models.Model):

    dep = models.CharField('部门', max_length=20)

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = '部门'

    def __str__(self):
        return self.dep

#用户表:用户名、角色、所在部门、密码
class User(models.Model):
    choices = ((True, "是"), (False, "否"))
    id = models.AutoField('序号',primary_key=True)
    name = models.CharField('用户名',max_length=128)
    grade = models.CharField('所属角色',max_length=20)
    dep = models.CharField('所属部门',max_length=20,null=True,blank=True)
    is_true = models.BooleanField(choices=choices, default=True, verbose_name='是否可用')
    password = models.CharField('密码',max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"
from django.db import models


class OpLogs(models.Model):
    """操作日志表"""

    id = models.AutoField(primary_key=True)
    re_time = models.CharField(max_length=32, verbose_name='请求时间')
    re_user = models.CharField(max_length=32, verbose_name='操作人')
    re_ip = models.CharField(max_length=32, verbose_name='请求IP')
    re_url = models.CharField(max_length=255, verbose_name='请求url')
    re_method = models.CharField(max_length=11, verbose_name='请求方法')
    re_content = models.TextField(null=True, verbose_name='请求参数')
    rp_content = models.TextField(null=True, verbose_name='响应参数')
    access_time = models.IntegerField(verbose_name='响应耗时/ms')

    class Meta:
        db_table = 'op_logs'


class AccessTimeOutLogs(models.Model):
    """超时操作日志表"""

    id = models.AutoField(primary_key=True)
    re_time = models.CharField(max_length=32, verbose_name='请求时间')
    re_user = models.CharField(max_length=32, verbose_name='操作人')
    re_ip = models.CharField(max_length=32, verbose_name='请求IP')
    re_url = models.CharField(max_length=255, verbose_name='请求url')
    re_method = models.CharField(max_length=11, verbose_name='请求方法')
    re_content = models.TextField(null=True, verbose_name='请求参数')
    rp_content = models.TextField(null=True, verbose_name='响应参数')
    access_time = models.IntegerField(verbose_name='响应耗时/ms')

    class Meta:
        db_table = 'access_timeout_logs'
