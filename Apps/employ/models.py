from django.db import models
from django.utils import timezone
from evm.models import *

#考评内容
class QContent(models.Model):
    title = models.CharField('测评项',max_length=40)
    detail = models.CharField('内容',max_length=128)
    a = models.CharField('A选项',max_length=40)
    b = models.CharField('B选项',max_length=40)
    c = models.CharField('C选项',max_length=40)
    d = models.CharField('D选项',max_length=40)


    class Meta:
        verbose_name = '考评内容'
        verbose_name_plural = '考评内容'

    def __str__(self):
        return self.title

#续聘意见
class QOpinion(models.Model):
    title = models.CharField('测评项',max_length=40)
    a = models.CharField('A选项',max_length=40)
    b = models.CharField('B选项',max_length=40)
    c = models.CharField('C选项',max_length=40)

    class Meta:
        verbose_name = '续聘意见'
        verbose_name_plural = '续聘意见'

    def __str__(self):
        return self.title

#测评对象
class EmpObject(models.Model):
    # 测评对象名称
    obj = models.CharField('测评对象', max_length=40)

    # 选择测评项
    pid1 = models.ManyToManyField(QContent,verbose_name='考评内容( 按住 Ctrl 键或 Shift 键来选择多项 )')
    pid2 = models.ManyToManyField(QOpinion,verbose_name='续聘意见')

    class Meta:
        verbose_name = '测评对象'
        verbose_name_plural = '测评对象'

    def __str__(self):
        return self.obj

#测评表
class EmpPaper(models.Model):
    choices = ((True, "是"), (False, "否"))
    id = models.AutoField('序号',primary_key=True)
    title = models.CharField('测评表名',max_length=40)
    obj = models.ManyToManyField(EmpObject,verbose_name='测评对象( 按住 Ctrl 键或 Shift 键来选择多项 )')
    is_true = models.BooleanField(choices=choices,default=True,verbose_name='是否可用')
    ctime = models.DateTimeField(default=timezone.now,verbose_name='测评时间')
    time = models.IntegerField('测评时长',help_text='单位是分钟')

    class Meta:
        verbose_name = '试用期满干部考核表'
        verbose_name_plural = '试用期满干部考核表'

    def __str__(self):
        return self.title

# 投票记录表
class EmpRecord(models.Model):
    id = models.AutoField('序号', primary_key=True)
    paper = models.ForeignKey(EmpPaper,on_delete=models.CASCADE,verbose_name='测评名称')
    obj = models.CharField('测评对象',max_length=40)
    user = models.CharField('用户名',max_length=40)
    grade = models.CharField('投票人角色',max_length=40)
    #考评内容
    q1 = models.CharField('德',max_length=20)
    q2 = models.CharField('能',max_length=20)
    q3 = models.CharField('勤',max_length=20)
    q4 = models.CharField('绩',max_length=20)
    q5 = models.CharField('廉',max_length=20)

    voted = models.CharField(max_length=8,verbose_name='续聘意见')
    time = models.DateTimeField(default=timezone.now,verbose_name="投票时间")

    class Meta:
        verbose_name = '届满考核_测评记录'
        verbose_name_plural = '届满考核_测评记录'

    def __str__(self):
        return '%s:%s:%s:%s:%s:%s:%s:%s' % (self.paper,self.obj,self.q1,self.q2,self.q3,self.q4,self.q5,self.voted)

#统计表:全体干部职工
class EmpAll(models.Model):
    id = models.AutoField('序号',primary_key=True)
    paper = models.CharField('测评名称',max_length=40)
    obj = models.CharField('测评对象', max_length=40,null=True)
    q11 = models.CharField('德-好',max_length=20)
    q12 = models.CharField('德-较好',max_length=20)
    q13 = models.CharField('德-一般',max_length=20)
    q14 = models.CharField('德-较差',max_length=20)
    q21 = models.CharField('能-好',max_length=20)
    q22 = models.CharField('能-较好',max_length=20)
    q23 = models.CharField('能-一般',max_length=20)
    q24 = models.CharField('能-较差',max_length=20)
    q31 = models.CharField('勤-好',max_length=20)
    q32 = models.CharField('勤-较好',max_length=20)
    q33 = models.CharField('勤-一般',max_length=20)
    q34 = models.CharField('勤-较差',max_length=20)
    q41 = models.CharField('绩-好',max_length=20)
    q42 = models.CharField('绩-较好',max_length=20)
    q43 = models.CharField('绩-一般',max_length=20)
    q44 = models.CharField('绩-较差',max_length=20)
    q51 = models.CharField('廉-好',max_length=20)
    q52 = models.CharField('廉-较好',max_length=20)
    q53 = models.CharField('廉-一般',max_length=20)
    q54 = models.CharField('廉-较差',max_length=20)
    vA = models.IntegerField(default=0,verbose_name='同意')
    vB = models.IntegerField(default=0,verbose_name='不同意')
    vC = models.IntegerField(default=0,verbose_name='弃权')

    class Meta:
        verbose_name = '届满考核_全体'
        verbose_name_plural = '届满考核_全体'


class EmpLeader(models.Model):
    id = models.AutoField('序号',primary_key=True)
    paper = models.CharField('测评名称', max_length=40)
    obj = models.CharField('测评对象', max_length=40,null=True)

    q11 = models.CharField('德-好', max_length=20)
    q12 = models.CharField('德-较好', max_length=20)
    q13 = models.CharField('德-一般', max_length=20)
    q14 = models.CharField('德-较差', max_length=20)
    q21 = models.CharField('能-好', max_length=20)
    q22 = models.CharField('能-较好', max_length=20)
    q23 = models.CharField('能-一般', max_length=20)
    q24 = models.CharField('能-较差', max_length=20)
    q31 = models.CharField('勤-好', max_length=20)
    q32 = models.CharField('勤-较好', max_length=20)
    q33 = models.CharField('勤-一般', max_length=20)
    q34 = models.CharField('勤-较差', max_length=20)
    q41 = models.CharField('绩-好', max_length=20)
    q42 = models.CharField('绩-较好', max_length=20)
    q43 = models.CharField('绩-一般', max_length=20)
    q44 = models.CharField('绩-较差', max_length=20)
    q51 = models.CharField('廉-好', max_length=20)
    q52 = models.CharField('廉-较好', max_length=20)
    q53 = models.CharField('廉-一般', max_length=20)
    q54 = models.CharField('廉-较差', max_length=20)
    vA = models.IntegerField(default=0, verbose_name='同意')
    vB = models.IntegerField(default=0, verbose_name='不同意')
    vC = models.IntegerField(default=0, verbose_name='弃权')

    class Meta:
        verbose_name = '届满考核_台领导'
        verbose_name_plural = '届满考核_台领导'

class EmpMiddle(models.Model):
    id = models.AutoField('序号',primary_key=True)
    paper = models.CharField('测评名称', max_length=40)
    obj = models.CharField('测评对象', max_length=40,null=True)
    q11 = models.CharField('德-好', max_length=20)
    q12 = models.CharField('德-较好', max_length=20)
    q13 = models.CharField('德-一般', max_length=20)
    q14 = models.CharField('德-较差', max_length=20)
    q21 = models.CharField('能-好', max_length=20)
    q22 = models.CharField('能-较好', max_length=20)
    q23 = models.CharField('能-一般', max_length=20)
    q24 = models.CharField('能-较差', max_length=20)
    q31 = models.CharField('勤-好', max_length=20)
    q32 = models.CharField('勤-较好', max_length=20)
    q33 = models.CharField('勤-一般', max_length=20)
    q34 = models.CharField('勤-较差', max_length=20)
    q41 = models.CharField('绩-好', max_length=20)
    q42 = models.CharField('绩-较好', max_length=20)
    q43 = models.CharField('绩-一般', max_length=20)
    q44 = models.CharField('绩-较差', max_length=20)
    q51 = models.CharField('廉-好', max_length=20)
    q52 = models.CharField('廉-较好', max_length=20)
    q53 = models.CharField('廉-一般', max_length=20)
    q54 = models.CharField('廉-较差', max_length=20)
    vA = models.IntegerField(default=0, verbose_name='同意')
    vB = models.IntegerField(default=0, verbose_name='不同意')
    vC = models.IntegerField(default=0, verbose_name='弃权')

    class Meta:
        verbose_name = '届满考核_中层干部'
        verbose_name_plural = '届满考核_中层干部'

class EmpStaff(models.Model):
    id = models.AutoField('序号',primary_key=True)
    paper = models.CharField('测评名称', max_length=40)
    obj = models.CharField('测评对象', max_length=40,null=True)
    q11 = models.CharField('德-好', max_length=20)
    q12 = models.CharField('德-较好', max_length=20)
    q13 = models.CharField('德-一般', max_length=20)
    q14 = models.CharField('德-较差', max_length=20)
    q21 = models.CharField('能-好', max_length=20)
    q22 = models.CharField('能-较好', max_length=20)
    q23 = models.CharField('能-一般', max_length=20)
    q24 = models.CharField('能-较差', max_length=20)
    q31 = models.CharField('勤-好', max_length=20)
    q32 = models.CharField('勤-较好', max_length=20)
    q33 = models.CharField('勤-一般', max_length=20)
    q34 = models.CharField('勤-较差', max_length=20)
    q41 = models.CharField('绩-好', max_length=20)
    q42 = models.CharField('绩-较好', max_length=20)
    q43 = models.CharField('绩-一般', max_length=20)
    q44 = models.CharField('绩-较差', max_length=20)
    q51 = models.CharField('廉-好', max_length=20)
    q52 = models.CharField('廉-较好', max_length=20)
    q53 = models.CharField('廉-一般', max_length=20)
    q54 = models.CharField('廉-较差', max_length=20)
    vA = models.IntegerField(default=0, verbose_name='同意')
    vB = models.IntegerField(default=0, verbose_name='不同意')
    vC = models.IntegerField(default=0, verbose_name='弃权')

    class Meta:
        verbose_name = '届满考核_普通职工'
        verbose_name_plural = '届满考核_普通职工'

