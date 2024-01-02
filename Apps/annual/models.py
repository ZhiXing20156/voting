from django.db import models
from django.utils import timezone
from evm.models import *

class Question1(models.Model):
    title = models.CharField('测评项',max_length=40)
    a = models.CharField('A选项',max_length=40)
    b = models.CharField('B选项',max_length=40)
    c = models.CharField('C选项',max_length=40)
    d = models.CharField('D选项',max_length=40)
    e = models.CharField('E选项',max_length=40)
    f = models.CharField('F选项',max_length=40)
    g = models.CharField('G选项',max_length=40)
    h = models.CharField('H选项',max_length=40)
    i = models.CharField('I选项',max_length=40)
    j = models.CharField('J选项',max_length=40)

    class Meta:
        verbose_name = '考评内容'
        verbose_name_plural = '考评内容'

    def __str__(self):
        return self.title

class Question2(models.Model):
    title = models.CharField('测评项',max_length=40)
    a = models.CharField('A选项',max_length=40)
    b = models.CharField('B选项',max_length=40)
    c = models.CharField('C选项',max_length=40)
    d = models.CharField('D选项',max_length=40)
    e = models.CharField('E选项',max_length=40)

    class Meta:
        verbose_name = '综合评价'
        verbose_name_plural = '综合评价'

    def __str__(self):
        return self.title

class Object(models.Model):
    obj = models.CharField('测评对象', max_length=40)
    dep = models.ForeignKey(Department,on_delete=models.CASCADE,verbose_name='所在部门')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE,verbose_name='角色')
    pid1 = models.ManyToManyField(Question1,verbose_name='考评内容( 按住 Ctrl 键或 Shift 键来选择多项 )') #从题库中选择测评项
    pid2 = models.ManyToManyField(Question2,verbose_name='综合评价')

    class Meta:
        verbose_name = '测评对象'
        verbose_name_plural = '测评对象'

    def __str__(self):
        return self.obj

class TestPaper(models.Model):
    choices = ((True, "是"), (False, "否"))
    id = models.AutoField('序号',primary_key=True)
    title = models.CharField('测评表名',max_length=40)
    obj = models.ManyToManyField(Object,verbose_name='测评对象( 按住 Ctrl 键或 Shift 键来选择多项 )')
    is_true = models.BooleanField(choices=choices,default=True,verbose_name='是否可用')
    ctime = models.DateTimeField(default=timezone.now,verbose_name='测评时间')
    time = models.IntegerField('测评时长',help_text='单位是分钟')
    num = models.IntegerField('优秀人数',default=0,null=True)

    class Meta:
        verbose_name = '年度考核表'
        verbose_name_plural = '年度考核表'

    def __str__(self):
        return self.title

class AnnualRecord(models.Model):
    id = models.AutoField('序号', primary_key=True)
    paper = models.ForeignKey(TestPaper,on_delete=models.CASCADE,verbose_name='测评名称')
    obj = models.CharField('测评对象',max_length=40)
    user = models.CharField('用户名',max_length=40)
    grade = models.CharField('投票人角色',max_length=40)
    dep = models.CharField('所在部门',max_length=40)
    score = models.FloatField('总分')
    q1 = models.IntegerField('德')
    q2 = models.IntegerField('能')
    q3 = models.IntegerField('勤')
    q4 = models.IntegerField('绩')
    q5 = models.IntegerField('学')
    q6 = models.IntegerField('廉')

    voted = models.CharField(max_length=8,blank=True,verbose_name='综合评价')
    time = models.DateTimeField(default=timezone.now,verbose_name="投票时间")

    class Meta:
        verbose_name = '年度考核_测评记录'
        verbose_name_plural = '年度考核_测评记录'

    def __str__(self):
        return '%s:%s:%s:%s' % (self.paper,self.obj,self.score,self.voted)

class AnnualAll(models.Model):
    id = models.AutoField('序号',primary_key=True)
    paper = models.CharField('测评名称',max_length=40)
    obj = models.CharField('测评对象', max_length=40,null=True)
    score = models.FloatField('得分')
    q1 = models.IntegerField('德')
    q2 = models.IntegerField('能')
    q3 = models.IntegerField('勤')
    q4 = models.IntegerField('绩')
    q5 = models.IntegerField('学')
    q6 = models.IntegerField('廉')
    voted_A = models.IntegerField(default=0,verbose_name='优秀')
    voted_B = models.IntegerField(default=0,verbose_name='合格')
    voted_C = models.IntegerField(default=0,verbose_name='基本合格')
    voted_D = models.IntegerField(default=0, verbose_name='不合格')
    voted_E = models.IntegerField(default=0, verbose_name='弃权')

    class Meta:
        verbose_name = '年度考核_全体'
        verbose_name_plural = '年度考核_全体'


class AnnualLeader(models.Model):
    id = models.AutoField('序号',primary_key=True)
    paper = models.CharField('测评名称', max_length=40)
    obj = models.CharField('测评对象', max_length=40,null=True)
    score = models.FloatField('得分')
    q1 = models.IntegerField('德')
    q2 = models.IntegerField('能')
    q3 = models.IntegerField('勤')
    q4 = models.IntegerField('绩')
    q5 = models.IntegerField('学')
    q6 = models.IntegerField('廉')
    voted_A = models.IntegerField(default=0,verbose_name='优秀')
    voted_B = models.IntegerField(default=0,verbose_name='合格')
    voted_C = models.IntegerField(default=0,verbose_name='基本合格')
    voted_D = models.IntegerField(default=0, verbose_name='不合格')
    voted_E = models.IntegerField(default=0, verbose_name='弃权')

    class Meta:
        verbose_name = '年度考核_台领导'
        verbose_name_plural = '年度考核_台领导'

class AnnualMiddle(models.Model):
    id = models.AutoField('序号',primary_key=True)
    paper = models.CharField('测评名称', max_length=40)
    obj = models.CharField('测评对象', max_length=40,null=True)
    score = models.FloatField('得分')
    q1 = models.IntegerField('德')
    q2 = models.IntegerField('能')
    q3 = models.IntegerField('勤')
    q4 = models.IntegerField('绩')
    q5 = models.IntegerField('学')
    q6 = models.IntegerField('廉')
    voted_A = models.IntegerField(default=0,verbose_name='优秀')
    voted_B = models.IntegerField(default=0,verbose_name='合格')
    voted_C = models.IntegerField(default=0,verbose_name='基本合格')
    voted_D = models.IntegerField(default=0, verbose_name='不合格')
    voted_E = models.IntegerField(default=0, verbose_name='弃权')

    class Meta:
        verbose_name = '年度考核_中层干部'
        verbose_name_plural = '年度考核_中层干部'

class AnnualStaff(models.Model):
    id = models.AutoField('序号',primary_key=True)
    paper = models.CharField('测评名称', max_length=40)
    obj = models.CharField('测评对象', max_length=40,null=True)
    score = models.FloatField('得分')
    q1 = models.IntegerField('德')
    q2 = models.IntegerField('能')
    q3 = models.IntegerField('勤')
    q4 = models.IntegerField('绩')
    q5 = models.IntegerField('学')
    q6 = models.IntegerField('廉')
    voted_A = models.IntegerField(default=0,verbose_name='优秀')
    voted_B = models.IntegerField(default=0,verbose_name='合格')
    voted_C = models.IntegerField(default=0,verbose_name='基本合格')
    voted_D = models.IntegerField(default=0, verbose_name='不合格')
    voted_E = models.IntegerField(default=0, verbose_name='弃权')

    class Meta:
        verbose_name = '年度考核_普通职工'
        verbose_name_plural = '年度考核_普通职工'
