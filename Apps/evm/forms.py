from django import forms
from .utils.bootstrap import BootstrapModelForm
from .models import *

'''
 placeholder属性为输入框提供占位符
 autofocus属性为用户名输入框自动聚焦
 password类型的input标签不会显示明文密码
'''

'''登录'''
class AdminUserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=128,widget=forms.TextInput(attrs=
                                                                                 {'class':'form-control',
                                                                                  'placeholder':'请输入用户名',
                                                                                  'autofocus':''}))
    password = forms.CharField(label='密码',max_length=256,widget=forms.PasswordInput(attrs=
                                                                                    {'class':'form-control',
                                                                                     'placeholder':'请输入密码'}))

'''注册'''
class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs=
                                                                                    {'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs=
                                                                                    {'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs=
                                                                                    {'class': 'form-control'}))

'''用户管理'''
class UserModelForm(BootstrapModelForm):

    grade = forms.ChoiceField(
        choices=(("台领导", "台领导"), ("中层干部", "中层干部"), ("普通职工", "普通职工")),
        label="所属角色",
        initial="台领导",
        widget=forms.widgets.Select()
    )
    class Meta:
        model = User
        #排除部门
        exclude = ["dep"]

'''角色管理'''
class GradeModelForm(BootstrapModelForm):
    class Meta:
        model = Grade
        fields = "__all__"

'''部门管理'''
class DepModelForm(BootstrapModelForm):
    class Meta:
        model = Department
        fields = "__all__"
