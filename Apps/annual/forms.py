from .utils.bootstrap import BootstrapModelForm
from .models import *
from django import forms

class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=128,widget=forms.TextInput(attrs=
                                                                                 {'class': 'form-control',
                                                                                  'placeholder': '请输入用户名',
                                                                                  'autofocus': ''}))

    password = forms.CharField(label='密码',max_length=256,widget=forms.PasswordInput(attrs=
                                                                                    { 'class': 'form-control',
                                                                                      'placeholder': '请输入密码'}))

class Q1ModelForm(BootstrapModelForm):

    title = forms.ChoiceField(
        choices = (("德", "德"),("能","能"),("勤","勤"),("绩","绩"),("学","学"),("廉","廉")),
        label = "测评项",
        initial = "德",
        widget = forms.widgets.Select()
    )
    a = forms.ChoiceField(
        choices = (("10", "10"),("9","9"),("8","8"),("7","7"),("6","6"),("5","5"),("4","4"),("3","3"),("2","2"),("1","1")),
        label = "A选项",
        initial = "10",
        widget = forms.widgets.Select()
    )
    b = forms.ChoiceField(
        choices = (("10", "10"),("9","9"),("8","8"),("7","7"),("6","6"),("5","5"),("4","4"),("3","3"),("2","2"),("1","1")),
        label="B选项",
        initial = "9",
        widget = forms.widgets.Select()
    )
    c = forms.ChoiceField(
        choices = (("10", "10"),("9","9"),("8","8"),("7","7"),("6","6"),("5","5"),("4","4"),("3","3"),("2","2"),("1","1")),
        label="C选项",
        initial ="8",
        widget = forms.widgets.Select()
    )
    d = forms.ChoiceField(
        choices = (("10", "10"),("9","9"),("8","8"),("7","7"),("6","6"),("5","5"),("4","4"),("3","3"),("2","2"),("1","1")),
        label = "D选项",
        initial = "7",
        widget = forms.widgets.Select()
    )
    e = forms.ChoiceField(
        choices = (("10", "10"),("9","9"),("8","8"),("7","7"),("6","6"),("5","5"),("4","4"),("3","3"),("2","2"),("1","1")),
        label="E选项",
        initial = "6",
        widget = forms.widgets.Select()
    )
    f = forms.ChoiceField(
        choices = (("10", "10"),("9","9"),("8","8"),("7","7"),("6","6"),("5","5"),("4","4"),("3","3"),("2","2"),("1","1")),
        label="F选项",
        initial ="5",
        widget = forms.widgets.Select()
    )
    g = forms.ChoiceField(
        choices = (("10", "10"),("9","9"),("8","8"),("7","7"),("6","6"),("5","5"),("4","4"),("3","3"),("2","2"),("1","1")),
        label = "G选项",
        initial = "4",
        widget = forms.widgets.Select()
    )
    h = forms.ChoiceField(
        choices = (("10", "10"),("9","9"),("8","8"),("7","7"),("6","6"),("5","5"),("4","4"),("3","3"),("2","2"),("1","1")),
        label="H选项",
        initial = "3",
        widget = forms.widgets.Select()
    )
    i = forms.ChoiceField(
        choices = (("10", "10"),("9","9"),("8","8"),("7","7"),("6","6"),("5","5"),("4","4"),("3","3"),("2","2"),("1","1")),
        label="I选项",
        initial ="2",
        widget = forms.widgets.Select()
    )
    j = forms.ChoiceField(
        choices = (("10", "10"),("9","9"),("8","8"),("7","7"),("6","6"),("5","5"),("4","4"),("3","3"),("2","2"),("1","1")),
        label="J选项",
        initial ="1",
        widget = forms.widgets.Select()
    )

    class Meta:
        model = Question1
        fields = "__all__"

class Q2ModelForm(BootstrapModelForm):

    title = forms.ChoiceField(
        choices = (("综合评价", "综合评价"),),
        label = "测评项",
        initial = "综合评价",
        widget = forms.widgets.Select()
    )
    a = forms.ChoiceField(
        choices = (("优秀", "优秀"),("合格","合格"),("基本合格","基本合格"),("不合格","不合格"),("弃权","弃权")),
        label = "A选项",
        initial = "优秀",
        widget = forms.widgets.Select()
    )
    b = forms.ChoiceField(
        choices = (("优秀", "优秀"),("合格","合格"),("基本合格","基本合格"),("不合格","不合格"),("弃权","弃权")),
        label="B选项",
        initial = "合格",
        widget = forms.widgets.Select()
    )
    c = forms.ChoiceField(
        choices = (("优秀", "优秀"),("合格","合格"),("基本合格","基本合格"),("不合格","不合格"),("弃权","弃权")),
        label="C选项",
        initial ="基本合格",
        widget = forms.widgets.Select()
    )
    d = forms.ChoiceField(
        choices = (("优秀", "优秀"),("合格","合格"),("基本合格","基本合格"),("不合格","不合格"),("弃权","弃权")),
        label = "D选项",
        initial = "不合格",
        widget = forms.widgets.Select()
    )
    e = forms.ChoiceField(
        choices = (("优秀", "优秀"),("合格","合格"),("基本合格","基本合格"),("不合格","不合格"),("弃权","弃权")),
        label="E选项",
        initial = "弃权",
        widget = forms.widgets.Select()
    )

    class Meta:
        model = Question2
        fields = "__all__"

class ObjModelForm(BootstrapModelForm):

    class Meta:
        model = Object
        fields = "__all__"

class PaperModelForm(BootstrapModelForm):
    class Meta:
        model = TestPaper
        fields = "__all__"

class RecordModelForm(BootstrapModelForm):
    class Meta:
        model = AnnualRecord
        fields = "__all__"
