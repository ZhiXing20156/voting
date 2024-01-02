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
    if request.session.get('recom_login', None):
        return HttpResponseRedirect(reverse('recom:index', args=()))
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
                    return render(request,'recom/login/login.html',locals())
            except:
                msg = '用户不存在！'
                return render(request, 'recom/login/login.html', locals())
            if user.password == password:  # 登录成功
                request.session['recom_login'] = True
                request.session['username'] = user.name
                return HttpResponseRedirect(reverse('recom:index', args=()))
            else:
                msg = '密码不正确！'
                return render(request, 'recom/login/login.html', locals())
        else:
            return render(request, 'recom/login/login.html', locals())

    login_form = UserForm()
    return render(request, 'recom/login/login.html', locals())


# 首页：测评信息
def index(request):
    if not request.session.get('recom_login', None):
        return HttpResponseRedirect(reverse('recom:login', args=()))
    else:
        username = request.session.get('username', None)
        user = User.objects.get(name=username)
        paper = RePaper.objects.filter(is_true=True)

        context = {
            'user': user,
            'paper': paper,
        }
    return render(request, 'recom/voting/index.html', context=context)

# 开始投票
def startVote(request):
    if not request.session.get('recom_login',None):
        return HttpResponseRedirect(reverse('recom:login', args=()))
    else:
        username = request.GET.get('name')
        id = request.GET.get('id')
        user = User.objects.get(name=username)

        paper = RePaper.objects.filter(id=id)

        context = {
            'user':user,
            'id':id,
            'paper':paper,
        }
    return render(request,'recom/voting/vote.html',context)

#投票统计
def voteCount(request):
    if request.method == 'POST':
        user = request.POST.get('name')
        id = request.POST.get('id')

        t = timezone.now()  # 获取当前时间
        now = t.strftime("%Y-%m-%d %H:%M:%S")  # 更改时间显示格式

        grade = User.objects.filter(name=user).values('grade')
        g = grade[0]['grade'] #获得投票人角色
        paper = RePaper.objects.filter(id=id)
        ReRecord.objects.filter(paper_id=id, user=user).delete()
        for p in paper.values('id'):
            pid = str(p['id'])
            obj = request.POST.getlist(pid)

            if obj == []:
                msg = "请选择您认为合适的人选 或 选择弃权！"
                return render(request, 'recom/voting/error.html', {"msg": msg})
            else:
                if '弃权' in obj:
                    if obj == ['弃权']:
                        ReRecord.objects.filter(paper_id=id,user=user).delete()
                        ReRecord.objects.create(paper_id=id, obj=obj, user=user, grade=g, time=now)
                    else:
                        msg = '弃权与其他选项不可同时选择，请返回修改！'
                        return render(request, 'recom/voting/error.html', {"msg": msg})
                else:
                    for o in obj:
                        ReRecord.objects.create(paper_id=id, obj=o, user=user, grade=g, time=now)


            # if obj is None:
            #     msg = "请选择您认为合适的人选！"
            #     return render(request, 'recom/voting/error.html', {"msg": msg})
            # else:
                # ReRecord.objects.filter(paper_id=id,user=user).delete()
                # ReRecord.objects.create(paper_id=id,obj=obj,user=user,grade=g,time=now)

        p_list = []
        r_list = []
        papers = RePaper.objects.filter(is_true=True).values('id')
        for p in papers:
            p = p['id']
            p_list.append(p)
        rs = ReRecord.objects.filter(user=user).values('paper_id')

        for r in rs:
            r = r['paper_id']
            r_list.append(r)


        p_list.sort()
        r = list(set(r_list)) #有多选，可先去重
        r.sort()
        if p_list == r:
            User.objects.filter(name=user).update(is_true=False)
            time.sleep(1)
            request.session.flush()
            return HttpResponseRedirect(reverse('recom:login', args=()))
        else:
            user = User.objects.get(name=user)
            paper = RePaper.objects.filter(is_true=True)

            context = {
                'user': user,
                'paper': paper,
            }

        return render(request,'recom/voting/index.html',context)


#投票用户退出登录
def logout(request):
    if not request.session.get('recom_login', None):
        return HttpResponseRedirect(reverse('recom:login', args=()))
    else:
        username = request.session.get('username', None)
        user = User.objects.get(name=username)
        paper = RePaper.objects.filter(is_true=True)
        for p in paper:

            if ReRecord.objects.filter(paper_id=p.id,user=user).exists():
                pass
            else:
                return JsonResponse({'code':1,'msg':p.title})

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

#职级
def rank_list(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        queryset = Rank.objects.all()
        form = RankModelForm
        context = {
            'rank_list': queryset,
            'form': form,
        }
    return render(request, 'recom/rank_list.html', context)

@csrf_exempt
def add_rank(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        form = RankModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            data_dict = {'status': True}
            return HttpResponse(json.dumps(data_dict))
        data_dict = {'status': False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))

def edit_rank_detail(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        uid = request.GET.get("uid")
        exists =Rank.objects.filter(id=uid).exists()
        if not exists:
            return HttpResponse(json.dumps({'status': False, 'error': "数据不存在"}))
        row_dict = Rank.objects.filter(id=uid).values('rank').first()
    return HttpResponse(json.dumps({'status': True, 'data': row_dict}))

@csrf_exempt
def edit_rank(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        uid = request.GET.get("uid")
        row_object = Rank.objects.filter(id=uid).first()
        if not row_object:
            return HttpResponse(json.dumps({'status': False, 'error_total': "数据不存在"}))
        form = RankModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            data_dict = {'status': True}
            return HttpResponse(json.dumps(data_dict))
        data_dict = {'status': False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))

def drop_rank(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        uid = request.GET.get("uid")
        exists = Rank.objects.filter(id=uid).exists()

        if not exists:
            return HttpResponse(json.dumps({'status': False, 'error': "数据不存在"}))
        Rank.objects.filter(id=uid).delete()
    return HttpResponse(json.dumps({'status': True}))

#测评对象
def obj_list(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        queryset = ReObj.objects.all()
        form = ReObjModelForm
        context = {
            'obj_list': queryset,
            'form': form,
        }
    return render(request, 'recom/obj_list.html', context)

@csrf_exempt
def add_obj(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        form = ReObjModelForm(data=request.POST)
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
        exists =ReObj.objects.filter(id=uid).exists()
        if not exists:
            return HttpResponse(json.dumps({'status': False, 'error': "数据不存在"}))
        row_dict = ReObj.objects.filter(id=uid).values('obj','sex','birth','age','work_time','dates','rank',
                   'status','post','time_in_post','job_title', 'degree','remark').first()
    return HttpResponse(json.dumps({'status': True, 'data': row_dict}))

@csrf_exempt
def edit_obj(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        uid = request.GET.get("uid")
        row_object = ReObj.objects.filter(id=uid).first()
        if not row_object:
            return HttpResponse(json.dumps({'status': False, 'error_total': "数据不存在"}))
        form = ReObjModelForm(data=request.POST, instance=row_object)
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
        exists = ReObj.objects.filter(id=uid).exists()

        if not exists:
            return HttpResponse(json.dumps({'status': False, 'error': "数据不存在"}))
        ReObj.objects.filter(id=uid).delete()
    return HttpResponse(json.dumps({'status': True}))

def delete_objs(request):
    if request.method == 'POST':
        values = request.POST.getlist('vals')
        for i in values:
            if i != '':
                drop_obj = ReObj.objects.get(id=i)
                drop_obj.delete()
        return HttpResponseRedirect(reverse('recom:obj_list', args=()))

#测评管理
def paper_list(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        queryset = RePaper.objects.all()
        form = RePaperModelForm
        context = {
            'paper_list': queryset,
            'form': form,
        }
    return render(request, 'recom/paper_list.html', context)

@csrf_exempt
def add_paper(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        form = RePaperModelForm(data=request.POST)
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
        exists =RePaper.objects.filter(id=uid).exists()
        if not exists:
            return HttpResponse(json.dumps({'status': False, 'error': "数据不存在"}))
        row_dict = RePaper.objects.filter(id=uid).values('title','post','num','is_true').first()
    return HttpResponse(json.dumps({'status': True, 'data': row_dict},cls=ComplexEncoder))

@csrf_exempt
def edit_paper(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        uid = request.GET.get("uid")
        row_object = RePaper.objects.filter(id=uid).first()
        if not row_object:
            return HttpResponse(json.dumps({'status': False, 'error_total': "数据不存在"}))
        form = RePaperModelForm(data=request.POST, instance=row_object)
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
        exists = RePaper.objects.filter(id=uid).exists()

        if not exists:
            return HttpResponse(json.dumps({'status': False, 'error': "数据不存在"}))
        RePaper.objects.filter(id=uid).delete()
    return HttpResponse(json.dumps({'status': True}))

#测评记录
def record_list(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        id = request.GET.get('id')
        queryset = ReRecord.objects.filter(paper_id=id)
        form = ReRecord
        context = {
            'record_list': queryset,
            'form': form,
        }
    return render(request, 'recom/record_list.html', context)

# 测评统计
def count(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        id = request.GET.get('id')

        user = User.objects.filter(is_true=True).count()

        objs = RePaper.objects.filter(id=id).values('obj__obj')

        #查看统计前将所有统计删除
        ReCount.objects.all().delete()
        obj_list = []
        for obj in objs:
            obj = obj['obj__obj']
            if obj != '弃权':
                obj_list.append(obj)
        for o in obj_list:
            p = ReObj.objects.filter(obj=o)
            post = p.values('post')[0]['post']

            vl = ReRecord.objects.filter(paper_id=id,obj=o,grade='台领导').count()
            vm = ReRecord.objects.filter(paper_id=id,obj=o,grade='中层干部').count()
            vs = ReRecord.objects.filter(paper_id=id,obj=o,grade='普通职工').count()
            vote = vl + vm + vs
            s = user
            ratio = '{:.2%}'.format(round(vote/s,4))#保留小数点后四位
            #ratio = round(vote/s,4)

            #生成统计前将原统计删除，防止重复统计
            ReCount.objects.filter(paper=id,obj=o).delete()
            ReCount.objects.create(paper=id,obj=o, vl=vl,vm=vm,vs=vs,post=post,vote=vote,sum=s,ratio=ratio)

    count = ReCount.objects.all()
    context = {
        'count':count,
    }
    return render(request,'recom/count.html',context=context)

#统计结果
def count_list(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        count_list = ReCount.objects.all()
        context = {
            'count_list':count_list,
        }
    return render(request,'recom/count_list.html',context)


#导出
def download(request):
    t = timezone.now()
    date = t.strftime("%Y%m%d")

    paper_id = ReCount.objects.all().values('paper')
    id = paper_id[0]['paper']
    title = RePaper.objects.filter(id=id).values('title')
    name = title[0]['title']

    # 指定数据类型
    response = HttpResponse(content_type='application/ms-excel')
    # 设置文件名称:测评表名称+当前日期
    response['Content-Disposition'] = "attachment; filename={0}_{1}.xls".format(escape_uri_path(name),date)
    # response['Content-Disposition'] = 'attachment; filename="result.xls"'
    # 创建工作簿
    wb = xlwt.Workbook(encoding='utf-8')

    font_style = xlwt.XFStyle()
    al = xlwt.Alignment()
    al.horz = 0x02
    al.vert = 0x01
    font_style.alignment = al
    # 二进制
    font_style.font.bold = True #粗体
    # 创建表
    ws = wb.add_sheet('统计结果')

    ws.write_merge(0, 0, 2, 4, '民主推荐得票数',font_style)
    ws.write_merge(0, 0, 5, 6, '得票率',font_style)

    row_num = 1

    # 表头内容
    columns = ['推荐人选','现工作岗位','台领导','中层干部','普通职工', '总票数','得票率']
    # 写进表头内容
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # 获取数据库数据
    rows = ReCount.objects.all().values_list('obj', 'post','vl','vm','vs','sum','ratio')

    # 遍历提取出来的内容
    for row in rows:
        row_num += 1
        # 逐行写入Excel
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


