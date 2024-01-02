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

'''竞聘岗位'''
class PostModelForm(BootstrapModelForm):
    class Meta:
        model = Post
        fields = "__all__"

'''测评对象'''
class QObjModelForm(BootstrapModelForm):

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
        model = QuesObj
        fields = "__all__"


'''测评票管理'''
class ComPaperModelForm(BootstrapModelForm):
    class Meta:
        model = Paper
        fields = "__all__"

'''测评记录'''
class CompRecordModelForm(BootstrapModelForm):
    class Meta:
        model = CompRecord
        fields = "__all__"
