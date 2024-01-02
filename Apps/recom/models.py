from django.db import models
from django.utils import timezone

class Rank(models.Model):
    rank = models.CharField('职级',max_length=40)

    class Meta:
        verbose_name = '职级'
        verbose_name_plural = '职级'

    def __str__(self):
        return self.rank

class ReObj(models.Model):
    obj = models.CharField('测评对象',max_length=40)
    sex = models.BooleanField('性别', choices=((0, '女'), (1, '男')),null=True,blank=True)
    birth = models.CharField('出生年月',max_length=40,null=True,blank=True)
    age = models.IntegerField('年龄',null=True,blank=True)
    work_time = models.CharField('参加工作时间',max_length=40,null=True,blank=True)
    dates = models.CharField('入局时间',max_length=40,null=True,blank=True)
    status = models.CharField('政治面貌',max_length=40,null=True,blank=True)
    post = models.CharField('现任职务',max_length=40,null=True,blank=True)
    time_in_post = models.CharField('任现职时间',max_length=40,null=True,blank=True)
    rank = models.ForeignKey(Rank,on_delete=models.CASCADE,verbose_name='现职级',null=True,blank=True)
    job_title = models.CharField('专业职务',max_length=40,null=True,blank=True)
    degree = models.CharField('文化程度',max_length=40,null=True,blank=True)

    remark = models.CharField('备注',max_length=128,null=True,blank=True)

    class Meta:
        verbose_name = '测评对象'
        verbose_name_plural = '测评对象'

    def __str__(self):
        return self.obj


class RePaper(models.Model):
    choices = ((True, "是"), (False, "否"))
    id = models.AutoField('序号',primary_key=True)
    title = models.CharField('测评表名',max_length=40)
    post = models.CharField('岗位名称',max_length=40)
    num = models.IntegerField('职数',default=1)
    rank = models.ForeignKey(Rank,on_delete=models.CASCADE,verbose_name='职级',null=True)
    obj = models.ManyToManyField(ReObj,verbose_name='测评对象')
    is_true = models.BooleanField(choices=choices,default=True,verbose_name='是否可用')
    c_time = models.DateTimeField(default=timezone.now,verbose_name='测评时间')

    class Meta:
        verbose_name = '民主推荐表'
        verbose_name_plural = '民主推荐表'

    def __str__(self):
        return self.title

# 投票记录表
class ReRecord(models.Model):
    id = models.AutoField('序号', primary_key=True)
    paper = models.ForeignKey(RePaper,on_delete=models.CASCADE,verbose_name='测评名称')
    obj = models.CharField('测评对象',max_length=40)
    user = models.CharField('投票人',max_length=40)
    grade = models.CharField('投票人角色',max_length=40)

    time = models.DateTimeField(default=timezone.now,verbose_name="投票时间")

    class Meta:
        verbose_name = '民主推荐_测评记录'
        verbose_name_plural = '民主推荐_测评记录'

    def __str__(self):
        return '%s:%s:%s' % (self.paper,self.obj,self.grade)

#统计表:全体干部职工
class ReCount(models.Model):
    id = models.AutoField('序号',primary_key=True)
    paper = models.CharField('测评名称',max_length=40)
    obj = models.CharField('测评对象', max_length=40)

    post = models.CharField('现工作岗位',max_length=40)

    vl = models.IntegerField(default=0,verbose_name='台领导')
    vm = models.IntegerField(default=0,verbose_name='中层干部')
    vs = models.IntegerField(default=0,verbose_name='普通职工')

    vote = models.IntegerField(default=0,verbose_name='得票数')
    sum = models.IntegerField(default=0,verbose_name='总票数')
    ratio  = models.CharField('得票率',max_length=40)


    class Meta:
        verbose_name = '民主推荐统计'
        verbose_name_plural = '民主推荐统计'
