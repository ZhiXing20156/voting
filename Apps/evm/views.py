from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
import logging
logger = logging.getLogger(__name__)
from django.shortcuts import render, HttpResponse
import json
import random
import xlrd
import xlwt
from django.db import transaction
from datetime import date, datetime
from .models import *
from django.views.decorators.csrf import csrf_exempt
#引入forms
from .forms import *

# 管理员登录
def login(request):
    if request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:index', args=()))
    if request.method == 'POST':
        login_form = AdminUserForm(request.POST)
        msg = '请检查填写的内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            try:
                user = AdminUser.objects.get(name=username)
            except:
                msg = '用户不存在！'
                return render(request, 'login/login.html', locals())

            if user.password == password:
                request.session['admin_login'] = True
                request.session['user_name'] = user.name
                return HttpResponseRedirect(reverse('evm:index', args=()))
            else:
                msg = '密码不正确！'
                return render(request, 'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())

    login_form = AdminUserForm()
    return render(request, 'login/login.html', locals())

# 管理员注册
def register(request):
    if request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:index', args=()))
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        msg= "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            if password1 != password2:
                msg = '两次输入的密码不同！'
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = AdminUser.objects.filter(name=username)
                if same_name_user:
                    msg = '用户名已经存在'
                    return render(request, 'login/register.html', locals())
                new_user = AdminUser()
                new_user.name = username
                new_user.password = password1
                new_user.save()
                return HttpResponseRedirect(reverse('evm:login', args=()))
        else:
            return render(request, 'login/register.html', locals())
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())

#角色
def grade_list(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        queryset = Grade.objects.all()
        form = GradeModelForm
        context = {
            'grade_list': queryset,
            'form': form,
        }
    return render(request, 'evm/grade_list.html', context)

@csrf_exempt
def add_grade(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        form = GradeModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            data_dict = {'status': True}
            return HttpResponse(json.dumps(data_dict))
        data_dict = {'status': False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))

def edit_detail(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:

        uid = request.GET.get("uid")
        exists =Grade.objects.filter(id=uid).exists()
        if not exists:
            return HttpResponse(json.dumps({'status': False, 'error': "数据不存在"}))
        row_dict = Grade.objects.filter(id=uid).values("grade", "weight").first()
    return HttpResponse(json.dumps({'status': True, 'data': row_dict}))

@csrf_exempt
def edit_grade(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        uid = request.GET.get("uid")
        row_object = Grade.objects.filter(id=uid).first()
        if not row_object:
            return HttpResponse(json.dumps({'status': False, 'error_total': "数据不存在"}))

        form = GradeModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            #form.instance.admin_id = request.session["info"]["id"]
            form.save()
            data_dict = {'status': True}
            return HttpResponse(json.dumps(data_dict))
        data_dict = {'status': False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))

def drop_grade(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        uid = request.GET.get("uid")
        exists = Grade.objects.filter(id=uid).exists()
        if not exists:
            return HttpResponse(json.dumps({'status': False, 'error': "数据不存在"}))
        Grade.objects.filter(id=uid).delete()
    return HttpResponse(json.dumps({'status': True}))

# 部门
def dep_list(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        queryset = Department.objects.all()
        form = DepModelForm
        context = {
            'dep_list': queryset,
            'form': form,
        }
    return render(request, 'evm/dep_list.html', context)

@csrf_exempt
def add_dep(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        form = DepModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            data_dict = {'status': True}
            return HttpResponse(json.dumps(data_dict))
        data_dict = {'status': False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))

def edit_dep_detail(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        uid = request.GET.get("uid")
        exists =Department.objects.filter(id=uid).exists()
        if not exists:
            return HttpResponse(json.dumps({'status': False, 'error': "数据不存在"}))
        row_dict = Department.objects.filter(id=uid).values("dep").first()
    return HttpResponse(json.dumps({'status': True, 'data': row_dict}))

@csrf_exempt
def edit_dep(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        uid = request.GET.get("uid")
        row_object = Department.objects.filter(id=uid).first()
        if not row_object:
            return HttpResponse(json.dumps({'status': False, 'error_total': "数据不存在"}))
        form = DepModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            data_dict = {'status': True}
            return HttpResponse(json.dumps(data_dict))
        data_dict = {'status': False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))

def drop_dep(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        uid = request.GET.get("uid")
        exists = Department.objects.filter(id=uid).exists()

        if not exists:
            return HttpResponse(json.dumps({'status': False, 'error': "数据不存在"}))
        Department.objects.filter(id=uid).delete()
    return HttpResponse(json.dumps({'status': True}))

def index(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        pass
    return render(request,'evm/index.html')

# 用户管理
def user_list(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        queryset = User.objects.all()
        form = UserModelForm
        grade = Grade.objects.all()
        context = {
            'user_list': queryset,
            'form': form,
            'grade_list':grade
        }
    return render(request, 'evm/user_list.html', context)

#批量创建用户
def create(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        if request.method == 'POST':
            nums = request.POST.getlist('grade')
            grades = Grade.objects.all().values('grade')
            t = timezone.now()
            date = t.strftime("%Y%m%d")
            # 指定数据类型
            response = HttpResponse(content_type='application/ms-excel')
            # 设置文件名称:测评表名称+当前日期
            response['Content-Disposition'] = "attachment; filename=user_{0}.xls".format(date)
            # response['Content-Disposition'] = 'attachment; filename="result.xls"'
            # 创建工作簿
            wb = xlwt.Workbook(encoding='utf-8')

            # 创建表
            ws = wb.add_sheet('user')
            row_num = 0
            font_style = xlwt.XFStyle()
            # 二进制
            font_style.font.bold = True
            # 表头内容
            columns = ['用户名', '密码',  '角色']
            # 写进表头内容
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)
            font_style = xlwt.XFStyle()
            datas = []
            for g in range(0,len(nums)):
                grade = grades[g]['grade']
                for i in range(1,int(nums[g])+1):
                    name = "491" + ''.join(random.sample("1234567890", 5))
                    pwd = ''.join(random.sample("1234567890", 6))
                    data = [name,pwd,grade]
                    datas.append(data)
            for d in datas:
                row_num += 1
                for col_num in range(len(d)):
                    ws.write(row_num,col_num,d[col_num],font_style)

            wb.save(response)
            return response

        return render(request,'evm/user_list.html')

#批量导入用户
def upload(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        if request.method == 'POST':
            f = request.FILES.get('file')
            #未选择文件
            if f is None:
                return HttpResponseRedirect(reverse('evm:user_list', args=()))
            else:
                excel_type = f.name.split('.')[1]
                print(excel_type)
                if excel_type in ['xlsx','xls']:
                    # 开始解析上传的excel表格
                    wb = xlrd.open_workbook(filename=None,file_contents=f.read())
                    table = wb.sheets()[0]
                    rows = table.nrows  # 总行数
                    try:
                        with transaction.atomic():  # 控制数据库事务交易
                            for i in range(1,rows):
                                row = table.row_values(i)
                                name = row[0] #姓名
                                pwd = row[1] #密码
                                # dep = row[2] #部门
                                grade = row[2] #角色

                                User.objects.create(name=name,grade=grade,password=pwd)

                            return HttpResponseRedirect(reverse('evm:user_list', args=()))
                    except:
                        logger.error('解析excel文件或者数据插入错误')

                    return render(request,'evm/user_list.html',{'message':'导入成功'})
                else:
                    logger.error('上传文件类型错误！')
                    return render(request,'evm/user_list.html',{'message':'导入失败'})

@csrf_exempt
def add_user(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        form = UserModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            data_dict = {'status': True}
            return HttpResponse(json.dumps(data_dict))
        data_dict = {'status': False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))

def edit_user_detail(request):
    """编辑前：传回原数据在显示框"""
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:

        uid = request.GET.get("uid")
        exists =User.objects.filter(id=uid).exists()
        if not exists:
            return HttpResponse(json.dumps({'status': False, 'error': "数据不存在"}))
        row_dict = User.objects.filter(id=uid).values("name", "grade","password").first()
        # 加上value后变成字典
        # form = OrderModelForm(instance=row_object), ajax无法识别
    return HttpResponse(json.dumps({'status': True, 'data': row_dict}))

@csrf_exempt
def edit_user(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        uid = request.GET.get("uid")
        row_object = User.objects.filter(id=uid).first()
        if not row_object:
            return HttpResponse(json.dumps({'status': False, 'error_total': "数据不存在"}))
            # 这里的数据不存在，与form.is_valid有本质不同。是整体效果，不是单个字段的问题
        form = UserModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            data_dict = {'status': True}
            return HttpResponse(json.dumps(data_dict))
        data_dict = {'status': False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))

def drop_user(request):
    """删除数据"""
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        uid = request.GET.get("uid")
        exists = User.objects.filter(id=uid).exists()

        if not exists:
            return HttpResponse(json.dumps({'status': False, 'error': "数据不存在"}))
        User.objects.filter(id=uid).delete()
    return HttpResponse(json.dumps({'status': True}))

def delete_users(request):
    if request.method == 'POST':
        values = request.POST.getlist('vals')
        for i in values:
            # 如果id不为空，获取该字段，并将其删除
            if i != '':
                drop_obj = User.objects.get(id=i)
                drop_obj.delete()
        return HttpResponseRedirect(reverse('evm:user_list', args=()))


# 管理员登出
def logout(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    request.session.flush()
    return HttpResponseRedirect(reverse('evm:login', args=()))

