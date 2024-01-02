from django.db import models
from django.utils import timezone

class Post(models.Model):
    post = models.CharField('竞聘岗位',max_length=40)
    num = models.IntegerField('职数',default=1)

    class Meta:
        verbose_name = '竞聘岗位'
        verbose_name_plural = '竞聘岗位'

    def __str__(self):
        return self.post

class QuesObj(models.Model):
    obj = models.CharField('测评对象',max_length=40)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,verbose_name='竞聘岗位')
    a = models.CharField('A选项',max_length=40)
    b = models.CharField('B选项', max_length=40)
    c = models.CharField('C选项', max_length=40)

    class Meta:
        verbose_name = '测评对象'
        verbose_name_plural = '测评对象'

    def __str__(self):
        return self.obj

class Paper(models.Model):
    choices = ((True, "是"), (False, "否"))
    id = models.AutoField('序号',primary_key=True)
    title = models.CharField('测评表名',max_length=40)
    obj = models.ManyToManyField(QuesObj, verbose_name='测评对象( 按住 Ctrl 键或 Shift 键来选择多项 )')
    is_true = models.BooleanField(choices=choices,default=True,verbose_name='是否可用')
    ctime = models.DateTimeField(default=timezone.now,verbose_name='测评时间')
    time = models.IntegerField('测评时长',help_text='单位是分钟')

    class Meta:
        verbose_name = '民主测评表'
        verbose_name_plural = '民主测评表'

    def __str__(self):
        return self.title

# 投票记录表
class CompRecord(models.Model):
    id = models.AutoField('序号', primary_key=True)
    paper = models.ForeignKey(Paper,on_delete=models.CASCADE,verbose_name='测评名称')
    obj = models.CharField('测评对象',max_length=40)
    user = models.CharField('投票人',max_length=40)
    grade = models.CharField('投票人角色',max_length=40)

    #投票项
    voted = models.CharField(max_length=40,verbose_name='测评意见')
    time = models.DateTimeField(default=timezone.now,verbose_name="投票时间")

    class Meta:
        verbose_name = '民主测评_测评记录'
        verbose_name_plural = '民主测评_测评记录'

    def __str__(self):
        return '%s:%s:%s:%s' % (self.paper,self.obj,self.voted,self.grade)

#统计表:全体干部职工
class CompAll(models.Model):
    id = models.AutoField('序号',primary_key=True)
    paper = models.CharField('测评名称',max_length=40)
    obj = models.CharField('测评对象', max_length=40,null=True)
    post = models.CharField('竞聘岗位',max_length=40,null=True)
    num = models.CharField('职数',max_length=40,null=True)

    vA = models.IntegerField(default=0,verbose_name='同意')
    vB = models.IntegerField(default=0,verbose_name='不同意')
    vC = models.IntegerField(default=0,verbose_name='弃权')

    class Meta:
        verbose_name = '民主测评_全体'
        verbose_name_plural = '民主测评_全体'

class CompLeader(models.Model):
    id = models.AutoField('序号',primary_key=True)
    paper = models.CharField('测评名称',max_length=40)
    obj = models.CharField('测评对象', max_length=40,null=True)
    post = models.CharField('竞聘岗位',max_length=40,null=True)
    num = models.CharField('职数',max_length=40,null=True)

    vA = models.IntegerField(default=0,verbose_name='同意')
    vB = models.IntegerField(default=0,verbose_name='不同意')
    vC = models.IntegerField(default=0,verbose_name='弃权')

    class Meta:
        verbose_name = '民主测评_台领导'
        verbose_name_plural = '民主测评_台领导'

class CompMiddle(models.Model):
    id = models.AutoField('序号',primary_key=True)
    paper = models.CharField('测评名称',max_length=40)
    obj = models.CharField('测评对象', max_length=40,null=True)
    post = models.CharField('竞聘岗位',max_length=40,null=True)
    num = models.CharField('职数',max_length=40,null=True)

    vA = models.IntegerField(default=0,verbose_name='同意')
    vB = models.IntegerField(default=0,verbose_name='不同意')
    vC = models.IntegerField(default=0,verbose_name='弃权')

    class Meta:
        verbose_name = '民主测评_中层干部'
        verbose_name_plural = '民主测评_中层干部'

class CompStaff(models.Model):
    id = models.AutoField('序号',primary_key=True)
    paper = models.CharField('测评名称',max_length=40)
    obj = models.CharField('测评对象', max_length=40,null=True)
    post = models.CharField('竞聘岗位',max_length=40,null=True)
    num = models.CharField('职数',max_length=40,null=True)

    vA = models.IntegerField(default=0,verbose_name='同意')
    vB = models.IntegerField(default=0,verbose_name='不同意')
    vC = models.IntegerField(default=0,verbose_name='弃权')

    class Meta:
        verbose_name = '民主测评_普通职工'
        verbose_name_plural = '民主测评_普通职工'