from .utils.bootstrap import BootstrapModelForm
from .models import *
from django import forms

'''投票用户
'''
class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=128,widget=forms.TextInput(attrs=
                                                                                 {'class': 'form-control',
                                                                                  'placeholder': '请输入用户名',
                                                                                  'autofocus': ''}))

    password = forms.CharField(label='密码',max_length=256,widget=forms.PasswordInput(attrs=
                                                                                    { 'class': 'form-control',
                                                                                      'placeholder': '请输入密码'}))

'''职级'''
class RankModelForm(BootstrapModelForm):
    class Meta:
        model = Rank
        fields = "__all__"

'''测评对象'''
class ReObjModelForm(BootstrapModelForm):

    remark = forms.CharField(
        label='备注',
        widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}),
        required=False
    )

    class Meta:
        model = ReObj
        fields = "__all__"


'''测评票管理'''
class RePaperModelForm(BootstrapModelForm):
    class Meta:
        model = RePaper

        fields = "__all__"

'''测评记录'''
class ReRecordModelForm(BootstrapModelForm):
    class Meta:
        model = ReRecord
        fields = "__all__"
