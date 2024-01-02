from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse
import logging
logger = logging.getLogger(__name__)
import xlwt
import time
from datetime import date, datetime
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import escape_uri_path
from django.http import JsonResponse
#引入forms
from .forms import *
import json
from django.urls import reverse
from .models import *
from evm.models import *

#投票用户登录
def login(request):
    # 不允许重复登录
    if request.session.get('comp_login', None):
        return HttpResponseRedirect(reverse('compete:index', args=()))
    if request.method == 'POST':
        login_form = UserForm(request.POST)
        msg = '请检查填写的内容'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            try:
                user = User.objects.get(name=username)
                if user.is_true is False:
                    msg = '您已完成投票，不能重复登录！'
                    return render(request,'compete/login/login.html',locals())
            except:
                msg = '用户不存在！'
                return render(request, 'compete/login/login.html', locals())
            if user.password == password:  # 登录成功
                request.session['comp_login'] = True
                request.session['username'] = user.name
                return HttpResponseRedirect(reverse('compete:index', args=()))
            else:
                msg = '密码不正确！'
                return render(request, 'compete/login/login.html', locals())
        else:
            return render(request, 'compete/login/login.html', locals())

    login_form = UserForm()
    return render(request, 'compete/login/login.html', locals())


# 首页：测评信息
def index(request):
    if not request.session.get('comp_login', None):
        return HttpResponseRedirect(reverse('compete:login', args=()))
    else:
        username = request.session.get('username', None)
        user = User.objects.get(name=username)
        paper = Paper.objects.filter(is_true=True)

        context = {
            'user': user,
            'paper': paper,
        }
    return render(request, 'compete/voting/index.html', context=context)

# 开始投票
def startVote(request):
    if not request.session.get('comp_login',None):
        return HttpResponseRedirect(reverse('compete:login', args=()))
    else:
        username = request.GET.get('name')
        id = request.GET.get('id')
        user = User.objects.get(name=username)

        paper = Paper.objects.filter(id=id)

        context = {
            'user':user,
            'id':id,
            'paper':paper,
        }
    return render(request,'compete/voting/vote.html',context)

#投票统计
def voteCount(request):
    if request.method == 'POST':
        user = request.POST.get('name')
        id = request.POST.get('id')

        t = timezone.now()  # 获取当前时间
        now = t.strftime("%Y-%m-%d %H:%M:%S")  # 更改时间显示格式

        grade = User.objects.filter(name=user).values('grade')
        g = grade[0]['grade'] #获得投票人角色
        objs = Paper.objects.filter(id=id).values("obj").values('obj__obj')
        obj_list = []
        for p in objs:
            obj = str(p['obj__obj']) #测评对象
            obj_list.append(obj)
            voted = request.POST.get(obj) #投票选项
            if voted is None:
                msg = "请对所有对象进行测评！"
                return render(request, 'compete/voting/error.html', {"msg": msg})
            else:

                CompRecord.objects.filter(paper_id=id,obj=obj,user=user).delete()
                CompRecord.objects.create(user=user,obj=obj,voted=voted,paper_id=id,grade=g,time=now) #记入数据库


        robjs = CompRecord.objects.filter(paper_id=id, user=user).values('obj')
        robj = []
        for obj in robjs:
            r = obj['obj']
            robj.append(r)

        obj_list.sort()  # sort()方法是在原地对列表排序，返回为None 。
        robj.sort()
        # 判断记录表中该用户的投票对象列表与测评表中应有的测评对象列表作比较
        if robj == obj_list:
            User.objects.filter(name=user).update(is_true=False)
            time.sleep(2)
            request.session.flush()
            return HttpResponseRedirect(reverse('compete:login', args=()))

    return render(request,'compete/voting/index.html')

#投票用户退出登录
def logout(request):
    if not request.session.get('comp_login', None):
        return HttpResponseRedirect(reverse('compete:login', args=()))
    else:
        username = request.session.get('username', None)
        user = User.objects.get(name=username)
        paper = Paper.objects.filter(is_true=True)
        for p in paper:
            for o in p.obj.all():
                if CompRecord.objects.filter(obj=o, user=user).exists():
                    pass
                else:
                    return JsonResponse({"code": 1, "msg": o.obj})
        # 用户更新为不可用
        User.objects.filter(name=user).update(is_true=False)
        request.session.flush()
        return JsonResponse({"code": 0})

'''重构JSON类'''
class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

#竞聘岗位
def post_list(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        queryset = Post.objects.all()
        form = PostModelForm
        context = {
            'post_list': queryset,
            'form': form,
        }
    return render(request, 'compete/post_list.html', context)

@csrf_exempt
def add_post(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        form = PostModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            data_dict = {'status': True}
            return HttpResponse(json.dumps(data_dict))
        data_dict = {'status': False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))

def edit_post_detail(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        uid = request.GET.get("uid")
        exists =Post.objects.filter(id=uid).exists()
        if not exists:
            return HttpResponse(json.dumps({'status': False, 'error': "数据不存在"}))
        row_dict = Post.objects.filter(id=uid).values('post','num').first()
    return HttpResponse(json.dumps({'status': True, 'data': row_dict}))

@csrf_exempt
def edit_post(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        uid = request.GET.get("uid")
        row_object = Post.objects.filter(id=uid).first()
        if not row_object:
            return HttpResponse(json.dumps({'status': False, 'error_total': "数据不存在"}))
        form = PostModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            data_dict = {'status': True}
            return HttpResponse(json.dumps(data_dict))
        data_dict = {'status': False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))

def drop_post(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        uid = request.GET.get("uid")
        exists = Post.objects.filter(id=uid).exists()

        if not exists:
            return HttpResponse(json.dumps({'status': False, 'error': "数据不存在"}))
        Post.objects.filter(id=uid).delete()
    return HttpResponse(json.dumps({'status': True}))

#测评对象
def obj_list(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        queryset = QuesObj.objects.all()
        form = QObjModelForm
        context = {
            'obj_list': queryset,
            'form': form,
        }
    return render(request, 'compete/obj_list.html', context)

@csrf_exempt
def add_obj(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        form = QObjModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            data_dict = {'status': True}
            return HttpResponse(json.dumps(data_dict))
        data_dict = {'status': False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))

def edit_obj_detail(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        uid = request.GET.get("uid")
        exists =QuesObj.objects.filter(id=uid).exists()
        if not exists:
            return HttpResponse(json.dumps({'status': False, 'error': "数据不存在"}))
        row_dict = QuesObj.objects.filter(id=uid).values('obj','post','a','b','c').first()
    return HttpResponse(json.dumps({'status': True, 'data': row_dict}))

@csrf_exempt
def edit_obj(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        uid = request.GET.get("uid")
        row_object = QuesObj.objects.filter(id=uid).first()
        if not row_object:
            return HttpResponse(json.dumps({'status': False, 'error_total': "数据不存在"}))
        form = QObjModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            data_dict = {'status': True}
            return HttpResponse(json.dumps(data_dict))
        data_dict = {'status': False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))

def drop_obj(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        uid = request.GET.get("uid")
        exists = QuesObj.objects.filter(id=uid).exists()

        if not exists:
            return HttpResponse(json.dumps({'status': False, 'error': "数据不存在"}))
        QuesObj.objects.filter(id=uid).delete()
    return HttpResponse(json.dumps({'status': True}))

def delete_objs(request):
    if request.method == 'POST':
        values = request.POST.getlist('vals')
        for i in values:
            if i != '':
                drop_obj = QuesObj.objects.get(id=i)
                drop_obj.delete()
        return HttpResponseRedirect(reverse('compete:obj_list', args=()))

#测评管理
def paper_list(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        queryset = Paper.objects.all()
        form = ComPaperModelForm
        context = {
            'paper_list': queryset,
            'form': form,
        }
    return render(request, 'compete/paper_list.html', context)

@csrf_exempt
def add_paper(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        form = ComPaperModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            data_dict = {'status': True}
            return HttpResponse(json.dumps(data_dict))
        data_dict = {'status': False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))

def edit_paper_detail(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        uid = request.GET.get("uid")
        exists =Paper.objects.filter(id=uid).exists()
        if not exists:
            return HttpResponse(json.dumps({'status': False, 'error': "数据不存在"}))
        row_dict = Paper.objects.filter(id=uid).values('title','obj','is_true').first()
    return HttpResponse(json.dumps({'status': True, 'data': row_dict},cls=ComplexEncoder))

@csrf_exempt
def edit_paper(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        uid = request.GET.get("uid")
        row_object = Paper.objects.filter(id=uid).first()
        if not row_object:
            return HttpResponse(json.dumps({'status': False, 'error_total': "数据不存在"}))
        form = ComPaperModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            data_dict = {'status': True}
            return HttpResponse(json.dumps(data_dict))
        data_dict = {'status': False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))

def drop_paper(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        uid = request.GET.get("uid")
        exists = Paper.objects.filter(id=uid).exists()

        if not exists:
            return HttpResponse(json.dumps({'status': False, 'error': "数据不存在"}))
        Paper.objects.filter(id=uid).delete()
    return HttpResponse(json.dumps({'status': True}))

#测评记录
def record_list(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        id = request.GET.get('id')
        queryset = CompRecord.objects.filter(paper_id=id)
        form = CompRecord
        context = {
            'record_list': queryset,
            'form': form,
        }
    return render(request, 'compete/record_list.html', context)

# 测评统计
def count(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        id = request.GET.get('id')

        objs = Paper.objects.filter(id=id).values('obj__obj')

        #查看统计前将所有统计删除
        CompAll.objects.all().delete()
        CompLeader.objects.all().delete()
        CompMiddle.objects.all().delete()
        CompStaff.objects.all().delete()
        for obj in objs:
            obj = obj['obj__obj']
            p = QuesObj.objects.filter(obj=obj)
            post = p.values('post__post')[0]['post__post']
            num = p.values('post__num')[0]['post__num']

            v1 = CompRecord.objects.filter(paper_id=id,obj=obj,voted='同意').count()
            v2 = CompRecord.objects.filter(paper_id=id,obj=obj,voted='不同意').count()
            v3 = CompRecord.objects.filter(paper_id=id,obj=obj,voted='弃权').count()

            #生成统计前将原统计删除，防止重复统计
            CompAll.objects.filter(paper=id,obj=obj).delete()
            CompAll.objects.create(paper=id,obj=obj, vA=v1,vB=v2,vC=v3,post=post,num=num)

            #台领导
            v11 = CompRecord.objects.filter(paper_id=id,obj=obj,voted='同意',grade='台领导').count()
            v12 = CompRecord.objects.filter(paper_id=id,obj=obj,voted='不同意',grade='台领导').count()
            v13 = CompRecord.objects.filter(paper_id=id,obj=obj,voted='弃权',grade='台领导').count()
            CompLeader.objects.filter(paper=id,obj=obj).delete()
            CompLeader.objects.create(paper=id,obj=obj,vA=v11,vB=v12, vC=v13,post=post,num=num)

            #中层干部
            v21 = CompRecord.objects.filter(paper_id=id, obj=obj, voted='同意', grade='中层干部').count()
            v22 = CompRecord.objects.filter(paper_id=id, obj=obj, voted='不同意', grade='中层干部').count()
            v23 = CompRecord.objects.filter(paper_id=id, obj=obj, voted='弃权', grade='中层干部').count()

            CompMiddle.objects.filter(paper=id, obj=obj).delete()
            CompMiddle.objects.create(paper=id, obj=obj,vA=v21,vB=v22, vC=v23,post=post,num=num)

            #普通职工
            v31 = CompRecord.objects.filter(paper_id=id, obj=obj, voted='同意', grade='普通职工').count()
            v32 = CompRecord.objects.filter(paper_id=id, obj=obj, voted='不同意', grade='普通职工').count()
            v33 = CompRecord.objects.filter(paper_id=id, obj=obj, voted='弃权', grade='普通职工').count()


            CompStaff.objects.filter(paper=id, obj=obj).delete()
            CompStaff.objects.create(paper=id,obj=obj,vA=v31, vB=v32, vC=v33,post=post,num=num)

    count = CompAll.objects.all()
    context = {
        'count':count,
    }
    return render(request,'compete/count/count.html',context=context)

#导出
def download(request):
    t = timezone.now()
    date = t.strftime("%Y%m%d")

    paper_id = CompAll.objects.all().values('paper')
    id = paper_id[0]['paper']
    title = Paper.objects.filter(id=id).values('title')
    name = title[0]['title']

    # 指定数据类型
    response = HttpResponse(content_type='application/ms-excel')
    # 设置文件名称:测评表名称+当前日期
    #解决：名称用中文报错
    response['Content-Disposition'] = "attachment; filename={0}_{1}.xls".format(escape_uri_path(name),date)
    #response['Content-Disposition'] = 'attachment; filename="result.xls"'
    # 创建工作簿
    wb = xlwt.Workbook(encoding='utf-8')

    # 创建表
    ws = wb.add_sheet('全体')
    ws_l = wb.add_sheet('台领导')
    ws_m = wb.add_sheet('中层干部')
    ws_s = wb.add_sheet('普通职工')

    row_num = 0
    rl_num = 0
    rm_num = 0
    rs_num =0
    font_style = xlwt.XFStyle()
    al = xlwt.Alignment()
    al.horz = 0x02
    al.vert = 0x01
    font_style.alignment = al
    # 二进制
    font_style.font.bold = True
    # 表头内容
    columns = ['竞聘岗位','职数','测评对象','同意','不同意','弃权']
    # 写进表头内容
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
        ws_l.write(rl_num, col_num, columns[col_num], font_style)
        ws_m.write(rm_num, col_num, columns[col_num], font_style)
        ws_s.write(rs_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    # 获取数据库数据
    rows = CompAll.objects.all().values_list('post','num','obj','vA', 'vB','vC')
    rl = CompLeader.objects.all().values_list('post','num','obj','vA', 'vB','vC')
    rm = CompMiddle.objects.all().values_list('post','num','obj','vA', 'vB','vC')
    rs = CompStaff.objects.all().values_list('post','num','obj','vA', 'vB','vC')
    # 遍历提取出来的内容
    for row in rows:
        row_num += 1
        # 逐行写入Excel
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    for row in rl:
        rl_num += 1
        # 逐行写入Excel
        for col_num in range(len(row)):
            ws_l.write(rl_num, col_num, row[col_num], font_style)
    for row in rm:
        rm_num += 1
        # 逐行写入Excel
        for col_num in range(len(row)):
            ws_m.write(rm_num, col_num, row[col_num], font_style)
    for row in rs:
        rs_num += 1
        # 逐行写入Excel
        for col_num in range(len(row)):
            ws_s.write(rs_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response

#统计结果
def count_all(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        count_all = CompAll.objects.all()
        context = {
            'count_all':count_all,
        }
    return render(request,'compete/count/count_all.html',context)

def count_leader(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        count_leader = CompLeader.objects.all()
        context = {
            'count_leader':count_leader,
        }
    return render(request,'compete/count/count_leader.html',context)

def count_middle(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        count_middle = CompMiddle.objects.all()
        context = {
            'count_middle':count_middle,
        }
    return render(request,'compete/count/count_middle.html',context=context)

def count_staff(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        count_staff = CompStaff.objects.all()
        context = {
            'count_staff':count_staff,
        }
    return render(request,'compete/count/count_staff.html',context=context)