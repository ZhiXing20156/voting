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

'''考评内容'''
class QConModelForm(BootstrapModelForm):

    a = forms.ChoiceField(
        choices = (("好", "好"),("较好","较好"),("一般","一般"),("较差","较差")),
        label = "A选项",
        initial = "好",
        widget = forms.widgets.Select()
    )
    b = forms.ChoiceField(
        choices = (("好", "好"),("较好","较好"),("一般","一般"),("较差","较差")),
        label="B选项",
        initial = "较好",
        widget = forms.widgets.Select()
    )
    c = forms.ChoiceField(
        choices = (("好", "好"),("较好","较好"),("一般","一般"),("较差","较差")),
        label="C选项",
        initial ="一般",
        widget = forms.widgets.Select()
    )
    d = forms.ChoiceField(
        choices = (("好", "好"),("较好","较好"),("一般","一般"),("较差","较差")),
        label="D选项",
        initial ="较差",
        widget = forms.widgets.Select()
    )

    class Meta:
        model = QContent
        fields = "__all__"

'''续聘意见'''
class QOpModelForm(BootstrapModelForm):

    title = forms.ChoiceField(
        choices = (("续聘意见", "续聘意见"),),
        label = "测评项",
        initial = "续聘意见",
        widget = forms.widgets.Select()
    )
    a = forms.ChoiceField(
        choices = (("同意", "同意"),("不同意","不同意"),("弃权","弃权")),
        label = "A选项",
        initial = "同意",
        widget = forms.widgets.Select()
    )
    b = forms.ChoiceField(
        choices = (("同意", "同意"),("不同意","不同意"),("弃权","弃权")),
        label="B选项",
        initial = "不同意",
        widget = forms.widgets.Select()
    )
    c = forms.ChoiceField(
        choices = (("同意", "同意"),("不同意","不同意"),("弃权","弃权")),
        label="C选项",
        initial ="弃权",
        widget = forms.widgets.Select()
    )
    class Meta:
        model = QOpinion
        fields = "__all__"

'''测评对象'''
class EmpObjModelForm(BootstrapModelForm):
    class Meta:
        model = EmpObject
        fields = "__all__"

'''测评票管理'''
class EmpPaperModelForm(BootstrapModelForm):
    class Meta:
        model = EmpPaper
        fields = "__all__"

'''测评记录'''
class EmpRecordModelForm(BootstrapModelForm):
    class Meta:
        model = EmpRecord
        fields = "__all__"
