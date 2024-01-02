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

#投票用户登录
def login(request):
    # 不允许重复登录
    if request.session.get('employ_login', None):
        return HttpResponseRedirect(reverse('employ:index', args=()))
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
                    return render(request,'employ/login/login.html',locals())
            except:
                msg = '用户不存在！'
                return render(request, 'employ/login/login.html', locals())
            if user.password == password:  # 登录成功
                request.session['employ_login'] = True
                request.session['username'] = user.name
                return HttpResponseRedirect(reverse('employ:index', args=()))
            else:
                msg = '密码不正确！'
                return render(request, 'employ/login/login.html', locals())
        else:
            return render(request, 'employ/login/login.html', locals())

    login_form = UserForm()
    return render(request, 'employ/login/login.html', locals())


# 首页：测评信息
def index(request):
    if not request.session.get('employ_login', None):
        return HttpResponseRedirect(reverse('employ:login', args=()))
    else:
        username = request.session.get('username', None)
        user = User.objects.get(name=username)
        paper = EmpPaper.objects.filter(is_true=True)

        context = {
            'user': user,
            'paper': paper,
        }
    return render(request, 'employ/voting/index.html', context=context)

# 测评对象列表
def detail(request):
    if not request.session.get('employ_login',None):
        return HttpResponseRedirect(reverse('employ:login', args=()))
    else:
        username = request.GET.get('name')
        id = request.GET.get('id')
        paper = EmpPaper.objects.filter(id=id)


        context = {
            'user': username,
            'id' : id,
            'paper': paper,
        }
    return render(request,'employ/voting/detail.html',context)

# 开始投票
def startVote(request):
    if not request.session.get('employ_login',None):
        return HttpResponseRedirect(reverse('employ:login', args=()))
    else:
        username = request.GET.get('name')
        id = request.GET.get('id')
        obj = request.GET.get('obj')
        user = User.objects.get(name=username)
        objs = EmpObject.objects.filter(obj=obj)

        context = {
            'user':user,
            'id':id,
            'paper':objs,
            'obj':obj,
        }
    return render(request,'employ/voting/vote.html',context=context)

# 投票统计
def voteCount(request):

    if request.method == 'POST':
        user = request.POST.get('name')
        obj = request.POST.get('obj')
        id = request.POST.get('id')

        t = timezone.now()  # 获取当前时间
        now = t.strftime("%Y-%m-%d %H:%M:%S")  # 更改时间显示格式
        grade = User.objects.filter(name=user).values('grade')
        g = grade[0]['grade']

        ques1 = EmpObject.objects.filter(obj=obj).values("pid1").values('pid1__title')

        ques2 = EmpObject.objects.filter(obj=obj).values("pid2").values('pid2__title')
        qid = ques2[0]['pid2__title']
        voted2 = request.POST.get(qid)

        if voted2 is None:
            msg = '请返回选择续聘意见！'
            return render(request, 'employ/voting/error.html', {"msg": msg})
        else:
            #将打分项与得分生成为元组，并转换为字典，获取各项值
            list = []
            for p in ques1:
                qid = str(p['pid1__title'])
                vote = request.POST.get(qid)

                if vote is None:
                    msg = "请对所有问题进行评价！"
                    return render(request, 'employ/voting/error.html', {"msg": msg})
                else:
                    data = (qid,vote)
                    list.append(data) #元组: [(a,b),(c,d)]
            dic = dict(list) #类型转换
            # 获取各项评价
            de = dic['德']
            neng = dic['能']
            qin = dic['勤']
            ji = dic['绩']
            lian = dic['廉']

            EmpRecord.objects.filter(paper_id=id, obj=obj, user=user).delete()
            EmpRecord.objects.create(user=user, voted=voted2, paper_id=id, obj=obj,grade=g,
                                                     time=now,q1=de,q2=neng,q3=qin,q4=ji,q5=lian)
        paper = EmpPaper.objects.filter(id=id)
        pobjs = paper.values('obj__obj')
        pobj = []
        for obj in pobjs:
            p = obj['obj__obj']
            pobj.append(p)
        robjs = EmpRecord.objects.filter(paper_id=id, user=user).values('obj')
        robj = []
        for obj in robjs:
            r = obj['obj']
            robj.append(r)

        pobj.sort()  # sort()方法是在原地对列表排序，返回为None 。
        robj.sort()
        # 判断记录表中该用户的投票对象列表与测评表中应有的测评对象列表作比较
        if robj == pobj:
            User.objects.filter(name=user).update(is_true=False)
            time.sleep(1)
            request.session.flush()
            return HttpResponseRedirect(reverse('employ:login', args=()))
        else:
            username = request.session.get('username', None)
            user = User.objects.get(name=username)
            paper = EmpPaper.objects.filter(is_true=True)
            context = {
                'user': user,
                'paper': paper,
            }

            return render(request, 'employ/voting/detail.html',context)

#投票用户退出登录
def logout(request):
    if not request.session.get('employ_login', None):
        return HttpResponseRedirect(reverse('employ:login', args=()))
    else:
        username = request.session.get('username', None)
        user = User.objects.get(name=username)
        paper = EmpPaper.objects.filter(is_true=True)
        for p in paper:
            for o in p.obj.all():
                if EmpRecord.objects.filter(obj=o, user=user).exists():
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
#考评内容
def qc_list(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        queryset = QContent.objects.all()
        form = QConModelForm
        context = {
            'qc_list': queryset,
            'form': form,
        }
    return render(request, 'employ/qc_list.html', context)

@csrf_exempt
def add_qc(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        form = QConModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            data_dict = {'status': True}
            return HttpResponse(json.dumps(data_dict))
        data_dict = {'status': False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))

def edit_qc_detail(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        uid = request.GET.get("uid")
        exists =QContent.objects.filter(id=uid).exists()
        if not exists:
            return HttpResponse(json.dumps({'status': False, 'error': "数据不存在"}))
        row_dict = QContent.objects.filter(id=uid).values('title','detail','a','b','c','d').first()
    return HttpResponse(json.dumps({'status': True, 'data': row_dict}))

@csrf_exempt
def edit_qc(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        uid = request.GET.get("uid")
        row_object = QContent.objects.filter(id=uid).first()
        if not row_object:
            return HttpResponse(json.dumps({'status': False, 'error_total': "数据不存在"}))
        form = QConModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            data_dict = {'status': True}
            return HttpResponse(json.dumps(data_dict))
        data_dict = {'status': False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))

def drop_qc(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        uid = request.GET.get("uid")
        exists = QContent.objects.filter(id=uid).exists()

        if not exists:
            return HttpResponse(json.dumps({'status': False, 'error': "数据不存在"}))
        QContent.objects.filter(id=uid).delete()
    return HttpResponse(json.dumps({'status': True}))

#续聘意见
def qo_list(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        queryset = QOpinion.objects.all()
        form = QOpModelForm
        context = {
            'qo_list': queryset,
            'form': form,
        }
    return render(request, 'employ/qo_list.html', context)

@csrf_exempt
def add_qo(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        form = QOpModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            data_dict = {'status': True}
            return HttpResponse(json.dumps(data_dict))
        data_dict = {'status': False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))

def edit_qo_detail(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        uid = request.GET.get("uid")
        exists =QOpinion.objects.filter(id=uid).exists()
        if not exists:
            return HttpResponse(json.dumps({'status': False, 'error': "数据不存在"}))
        row_dict = QOpinion.objects.filter(id=uid).values('title','a','b','c').first()
    return HttpResponse(json.dumps({'status': True, 'data': row_dict}))

@csrf_exempt
def edit_qo(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        uid = request.GET.get("uid")
        row_object = QOpinion.objects.filter(id=uid).first()
        if not row_object:
            return HttpResponse(json.dumps({'status': False, 'error_total': "数据不存在"}))
        form = QOpModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            data_dict = {'status': True}
            return HttpResponse(json.dumps(data_dict))
        data_dict = {'status': False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))

def drop_qo(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        uid = request.GET.get("uid")
        exists = QOpinion.objects.filter(id=uid).exists()

        if not exists:
            return HttpResponse(json.dumps({'status': False, 'error': "数据不存在"}))
        QOpinion.objects.filter(id=uid).delete()
    return HttpResponse(json.dumps({'status': True}))

#测评对象
def obj_list(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        queryset = EmpObject.objects.all()
        form = EmpObjModelForm
        context = {
            'obj_list': queryset,
            'form': form,
        }
    return render(request, 'employ/obj_list.html', context)

@csrf_exempt
def add_obj(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        form = EmpObjModelForm(data=request.POST)
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
        exists =EmpObject.objects.filter(id=uid).exists()
        if not exists:
            return HttpResponse(json.dumps({'status': False, 'error': "数据不存在"}))
        row_dict = EmpObject.objects.filter(id=uid).values('obj','pid1','pid2').first()
    return HttpResponse(json.dumps({'status': True, 'data': row_dict}))

@csrf_exempt
def edit_obj(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        uid = request.GET.get("uid")
        row_object = EmpObject.objects.filter(id=uid).first()
        if not row_object:
            return HttpResponse(json.dumps({'status': False, 'error_total': "数据不存在"}))
        form = EmpObjModelForm(data=request.POST, instance=row_object)
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
        exists = EmpObject.objects.filter(id=uid).exists()

        if not exists:
            return HttpResponse(json.dumps({'status': False, 'error': "数据不存在"}))
        EmpObject.objects.filter(id=uid).delete()
    return HttpResponse(json.dumps({'status': True}))

def delete_objs(request):
    if request.method == 'POST':
        values = request.POST.getlist('vals')
        for i in values:
            if i != '':
                drop_obj = EmpObject.objects.get(id=i)
                drop_obj.delete()
        return HttpResponseRedirect(reverse('employ:obj_list', args=()))

#测评管理
def paper_list(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        queryset = EmpPaper.objects.all()
        form = EmpPaperModelForm
        context = {
            'paper_list': queryset,
            'form': form,
        }
    return render(request, 'employ/paper_list.html', context)

@csrf_exempt
def add_paper(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        form = EmpPaperModelForm(data=request.POST)
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
        exists =EmpPaper.objects.filter(id=uid).exists()
        if not exists:
            return HttpResponse(json.dumps({'status': False, 'error': "数据不存在"}))
        row_dict = EmpPaper.objects.filter(id=uid).values('title','obj','is_true').first()
    return HttpResponse(json.dumps({'status': True, 'data': row_dict},cls=ComplexEncoder))

@csrf_exempt
def edit_paper(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        uid = request.GET.get("uid")
        row_object = EmpPaper.objects.filter(id=uid).first()
        if not row_object:
            return HttpResponse(json.dumps({'status': False, 'error_total': "数据不存在"}))
        form = EmpPaperModelForm(data=request.POST, instance=row_object)
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
        exists = EmpPaper.objects.filter(id=uid).exists()

        if not exists:
            return HttpResponse(json.dumps({'status': False, 'error': "数据不存在"}))
        EmpPaper.objects.filter(id=uid).delete()
    return HttpResponse(json.dumps({'status': True}))

#测评记录
def record_list(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        id = request.GET.get('id')
        queryset = EmpRecord.objects.filter(paper_id=id)
        form = EmpRecordModelForm
        context = {
            'record_list': queryset,
            'form': form,
        }
    return render(request, 'employ/record_list.html', context)

# 测评统计
def count(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        id = request.GET.get('id')
        objs = EmpPaper.objects.filter(id=id).values('obj__obj')

        #查看统计前将所有统计删除
        EmpAll.objects.all().delete()
        EmpLeader.objects.all().delete()
        EmpMiddle.objects.all().delete()
        EmpStaff.objects.all().delete()

        for obj in objs:
            obj = obj['obj__obj']
            #德
            v11 = EmpRecord.objects.filter(paper_id=id,obj=obj,q1='好').count()
            v12 = EmpRecord.objects.filter(paper_id=id,obj=obj,q1='较好').count()
            v13 = EmpRecord.objects.filter(paper_id=id,obj=obj,q1='一般').count()
            v14 = EmpRecord.objects.filter(paper_id=id,obj=obj,q1='较差').count()
            #能
            v21 = EmpRecord.objects.filter(paper_id=id,obj=obj,q2='好').count()
            v22 = EmpRecord.objects.filter(paper_id=id,obj=obj,q2='较好').count()
            v23 = EmpRecord.objects.filter(paper_id=id,obj=obj,q2='一般').count()
            v24 = EmpRecord.objects.filter(paper_id=id,obj=obj,q2='较差').count()
            #勤
            v31 = EmpRecord.objects.filter(paper_id=id,obj=obj,q3='好').count()
            v32 = EmpRecord.objects.filter(paper_id=id,obj=obj,q3='较好').count()
            v33 = EmpRecord.objects.filter(paper_id=id,obj=obj,q3='一般').count()
            v34 = EmpRecord.objects.filter(paper_id=id,obj=obj,q3='较差').count()
            #绩
            v41 = EmpRecord.objects.filter(paper_id=id,obj=obj,q4='好').count()
            v42 = EmpRecord.objects.filter(paper_id=id,obj=obj,q4='较好').count()
            v43 = EmpRecord.objects.filter(paper_id=id,obj=obj,q4='一般').count()
            v44 = EmpRecord.objects.filter(paper_id=id,obj=obj,q4='较差').count()
            #廉
            v51 = EmpRecord.objects.filter(paper_id=id,obj=obj,q5='好').count()
            v52 = EmpRecord.objects.filter(paper_id=id,obj=obj,q5='较好').count()
            v53 = EmpRecord.objects.filter(paper_id=id,obj=obj,q5='一般').count()
            v54 = EmpRecord.objects.filter(paper_id=id,obj=obj,q5='较差').count()

            va = EmpRecord.objects.filter(paper_id=id,obj=obj,voted='同意').count()
            vb = EmpRecord.objects.filter(paper_id=id,obj=obj,voted='不同意').count()
            vc = EmpRecord.objects.filter(paper_id=id,obj=obj,voted='弃权').count()

            #生成统计前将原统计删除，防止重复统计
            EmpAll.objects.filter(paper=id,obj=obj).delete()
            EmpAll.objects.create(paper=id,obj=obj,q11=v11,q12=v12,q13=v13,q14=v14,q21=v21,q22=v22,q23=v23,
                                  q24=v24,q31=v31,q32=v32,q33=v33,q34=v34,q41=v41,q42=v42,q43=v43,q44=v44,
                                  q51=v51,q52=v52,q53=v53,q54=v54,vA=va,vB=vb,vC=vc)
            #台领导
            # 德
            v111 = EmpRecord.objects.filter(paper_id=id, obj=obj, q1='好',grade='台领导').count()
            v121 = EmpRecord.objects.filter(paper_id=id, obj=obj, q1='较好',grade='台领导').count()
            v131 = EmpRecord.objects.filter(paper_id=id, obj=obj, q1='一般',grade='台领导').count()
            v141 = EmpRecord.objects.filter(paper_id=id, obj=obj, q1='较差',grade='台领导').count()
            # 能
            v211 = EmpRecord.objects.filter(paper_id=id, obj=obj, q2='好',grade='台领导').count()
            v221 = EmpRecord.objects.filter(paper_id=id, obj=obj, q2='较好',grade='台领导').count()
            v231 = EmpRecord.objects.filter(paper_id=id, obj=obj, q2='一般',grade='台领导').count()
            v241 = EmpRecord.objects.filter(paper_id=id, obj=obj, q2='较差',grade='台领导').count()
            # 勤
            v311 = EmpRecord.objects.filter(paper_id=id, obj=obj, q3='好',grade='台领导').count()
            v321 = EmpRecord.objects.filter(paper_id=id, obj=obj, q3='较好',grade='台领导').count()
            v331 = EmpRecord.objects.filter(paper_id=id, obj=obj, q3='一般',grade='台领导').count()
            v341 = EmpRecord.objects.filter(paper_id=id, obj=obj, q3='较差',grade='台领导').count()
            # 绩
            v411 = EmpRecord.objects.filter(paper_id=id, obj=obj, q4='好',grade='台领导').count()
            v421 = EmpRecord.objects.filter(paper_id=id, obj=obj, q4='较好',grade='台领导').count()
            v431 = EmpRecord.objects.filter(paper_id=id, obj=obj, q4='一般',grade='台领导').count()
            v441 = EmpRecord.objects.filter(paper_id=id, obj=obj, q4='较差',grade='台领导').count()
            # 廉
            v511 = EmpRecord.objects.filter(paper_id=id, obj=obj, q5='好',grade='台领导').count()
            v521 = EmpRecord.objects.filter(paper_id=id, obj=obj, q5='较好',grade='台领导').count()
            v531 = EmpRecord.objects.filter(paper_id=id, obj=obj, q5='一般',grade='台领导').count()
            v541 = EmpRecord.objects.filter(paper_id=id, obj=obj, q5='较差',grade='台领导').count()

            v1a = EmpRecord.objects.filter(paper_id=id, obj=obj, voted='同意',grade='台领导').count()
            v1b = EmpRecord.objects.filter(paper_id=id, obj=obj, voted='不同意',grade='台领导').count()
            v1c = EmpRecord.objects.filter(paper_id=id, obj=obj, voted='弃权',grade='台领导').count()

            # 生成统计前将原统计删除，防止重复统计
            EmpLeader.objects.filter(paper=id, obj=obj).delete()
            EmpLeader.objects.create(paper=id,obj=obj,q11=v111,q12=v121,q13=v131,q14=v141,q21=v211,q22=v221,
                                     q23=v231,q24=v241,q31=v311,q32=v321,q33=v331,q34=v341,q41=v411,q42=v421,
                                     q43=v431,q44=v441,q51=v511,q52=v521,q53=v531,q54=v541,vA=v1a,vB=v1b,vC=v1c)

            v112 = EmpRecord.objects.filter(paper_id=id, obj=obj, q1='好', grade='中层干部').count()
            v122 = EmpRecord.objects.filter(paper_id=id, obj=obj, q1='较好', grade='中层干部').count()
            v132 = EmpRecord.objects.filter(paper_id=id, obj=obj, q1='一般', grade='中层干部').count()
            v142 = EmpRecord.objects.filter(paper_id=id, obj=obj, q1='较差', grade='中层干部').count()
            # 能
            v212 = EmpRecord.objects.filter(paper_id=id, obj=obj, q2='好', grade='中层干部').count()
            v222 = EmpRecord.objects.filter(paper_id=id, obj=obj, q2='较好', grade='中层干部').count()
            v232 = EmpRecord.objects.filter(paper_id=id, obj=obj, q2='一般', grade='中层干部').count()
            v242 = EmpRecord.objects.filter(paper_id=id, obj=obj, q2='较差', grade='中层干部').count()
            # 勤
            v312 = EmpRecord.objects.filter(paper_id=id, obj=obj, q3='好', grade='中层干部').count()
            v322 = EmpRecord.objects.filter(paper_id=id, obj=obj, q3='较好', grade='中层干部').count()
            v332 = EmpRecord.objects.filter(paper_id=id, obj=obj, q3='一般', grade='中层干部').count()
            v342 = EmpRecord.objects.filter(paper_id=id, obj=obj, q3='较差', grade='中层干部').count()
            # 绩
            v412 = EmpRecord.objects.filter(paper_id=id, obj=obj, q4='好', grade='中层干部').count()
            v422 = EmpRecord.objects.filter(paper_id=id, obj=obj, q4='较好', grade='中层干部').count()
            v432 = EmpRecord.objects.filter(paper_id=id, obj=obj, q4='一般', grade='中层干部').count()
            v442 = EmpRecord.objects.filter(paper_id=id, obj=obj, q4='较差', grade='中层干部').count()
            # 廉
            v512 = EmpRecord.objects.filter(paper_id=id, obj=obj, q5='好', grade='中层干部').count()
            v522 = EmpRecord.objects.filter(paper_id=id, obj=obj, q5='较好', grade='中层干部').count()
            v532 = EmpRecord.objects.filter(paper_id=id, obj=obj, q5='一般', grade='中层干部').count()
            v542 = EmpRecord.objects.filter(paper_id=id, obj=obj, q5='较差', grade='中层干部').count()

            v2a = EmpRecord.objects.filter(paper_id=id, obj=obj, voted='同意', grade='中层干部').count()
            v2b = EmpRecord.objects.filter(paper_id=id, obj=obj, voted='不同意', grade='中层干部').count()
            v2c = EmpRecord.objects.filter(paper_id=id, obj=obj, voted='弃权', grade='中层干部').count()

            # 生成统计前将原统计删除，防止重复统计
            EmpMiddle.objects.filter(paper=id, obj=obj).delete()
            EmpMiddle.objects.create(paper=id,obj=obj,q11=v112,q12=v122,q13=v132,q14=v142,q21=v212,q22=v222,
                                     q23=v232,q24=v242,q31=v312,q32=v322,q33=v332,q34=v342,q41=v412,q42=v422,
                                     q43=v432,q44=v442,q51=v512,q52=v522,q53=v532,q54=v542,vA=v2a,vB=v2b,vC=v2c)

            v113 = EmpRecord.objects.filter(paper_id=id, obj=obj, q1='好', grade='普通职工').count()
            v123 = EmpRecord.objects.filter(paper_id=id, obj=obj, q1='较好', grade='普通职工').count()
            v133 = EmpRecord.objects.filter(paper_id=id, obj=obj, q1='一般', grade='普通职工').count()
            v143 = EmpRecord.objects.filter(paper_id=id, obj=obj, q1='较差', grade='普通职工').count()
            # 能
            v213 = EmpRecord.objects.filter(paper_id=id, obj=obj, q2='好', grade='普通职工').count()
            v223 = EmpRecord.objects.filter(paper_id=id, obj=obj, q2='较好', grade='普通职工').count()
            v233 = EmpRecord.objects.filter(paper_id=id, obj=obj, q2='一般', grade='普通职工').count()
            v243 = EmpRecord.objects.filter(paper_id=id, obj=obj, q2='较差', grade='普通职工').count()
            # 勤
            v313 = EmpRecord.objects.filter(paper_id=id, obj=obj, q3='好', grade='普通职工').count()
            v323 = EmpRecord.objects.filter(paper_id=id, obj=obj, q3='较好', grade='普通职工').count()
            v333 = EmpRecord.objects.filter(paper_id=id, obj=obj, q3='一般', grade='普通职工').count()
            v343 = EmpRecord.objects.filter(paper_id=id, obj=obj, q3='较差', grade='普通职工').count()
            # 绩
            v413 = EmpRecord.objects.filter(paper_id=id, obj=obj, q4='好', grade='普通职工').count()
            v423 = EmpRecord.objects.filter(paper_id=id, obj=obj, q4='较好', grade='普通职工').count()
            v433 = EmpRecord.objects.filter(paper_id=id, obj=obj, q4='一般', grade='普通职工').count()
            v443 = EmpRecord.objects.filter(paper_id=id, obj=obj, q4='较差', grade='普通职工').count()
            # 廉
            v513 = EmpRecord.objects.filter(paper_id=id, obj=obj, q5='好', grade='普通职工').count()
            v523 = EmpRecord.objects.filter(paper_id=id, obj=obj, q5='较好', grade='普通职工').count()
            v533 = EmpRecord.objects.filter(paper_id=id, obj=obj, q5='一般', grade='普通职工').count()
            v543 = EmpRecord.objects.filter(paper_id=id, obj=obj, q5='较差', grade='普通职工').count()

            v3a = EmpRecord.objects.filter(paper_id=id, obj=obj, voted='同意', grade='普通职工').count()
            v3b = EmpRecord.objects.filter(paper_id=id, obj=obj, voted='不同意', grade='普通职工').count()
            v3c = EmpRecord.objects.filter(paper_id=id, obj=obj, voted='弃权', grade='普通职工').count()

            # 生成统计前将原统计删除，防止重复统计
            EmpStaff.objects.filter(paper=id, obj=obj).delete()
            EmpStaff.objects.create(paper=id, obj=obj, q11=v113, q12=v123, q13=v133, q14=v143, q21=v213, q22=v223,
                                  q23=v233, q24=v243, q31=v313, q32=v323, q33=v333, q34=v343, q41=v413, q42=v423,
                                  q43=v433, q44=v443,q51=v513, q52=v523, q53=v533, q54=v543, vA=v3a, vB=v3b, vC=v3c)

    count = EmpAll.objects.all()
    context = {
        'count':count,
    }
    return render(request,'employ/count/count.html',context=context)

#导出
def download(request):
    t = timezone.now()
    date = t.strftime("%Y%m%d")

    paper_id = EmpAll.objects.all().values('paper')
    id = paper_id[0]['paper']
    title = EmpPaper.objects.filter(id=id).values('title')
    name = title[0]['title']

    # 指定数据类型
    response = HttpResponse(content_type='application/ms-excel')
    # 设置文件名称:测评表名称+当前日期
    response['Content-Disposition'] = "attachment; filename={0}_{1}.xls".format(escape_uri_path(name),date)
    # response['Content-Disposition'] = 'attachment; filename="result.xls"'
    # 创建工作簿
    wb = xlwt.Workbook(encoding='utf-8')

    # 创建表
    ws = wb.add_sheet('全体')
    ws_l = wb.add_sheet('台领导')
    ws_m = wb.add_sheet('中层干部')
    ws_s = wb.add_sheet('普通职工')

    row_num = 1
    rl_num = 1
    rm_num = 1
    rs_num =1
    font_style = xlwt.XFStyle()

    al = xlwt.Alignment()
    al.horz = 0x02
    al.vert = 0x01
    font_style.alignment = al
    # 二进制
    font_style.font.bold = True #粗体
    # 表头内容
    columns = ['内容','好','较好','一般','较差', '好','较好','一般','较差', '好','较好','一般','较差', '好','较好',
               '一般','较差','好','较好','一般','较差','同意','不同意','弃权']
    # 写进表头内容
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
        ws_l.write(rl_num, col_num, columns[col_num], font_style)
        ws_m.write(rm_num, col_num, columns[col_num], font_style)
        ws_s.write(rs_num, col_num, columns[col_num], font_style)

    ws.write_merge(0, 0, 1, 4, '德',font_style)
    ws.write_merge(0, 0, 5, 8, '能',font_style)
    ws.write_merge(0, 0, 9, 12, '勤',font_style)
    ws.write_merge(0, 0, 13, 16, '绩',font_style)
    ws.write_merge(0, 0, 17, 20, '廉',font_style)
    ws.write_merge(0, 0, 21, 23, '续聘意见',font_style)

    ws_l.write_merge(0, 0, 1, 4, '德',font_style)
    ws_l.write_merge(0, 0, 5, 8, '能',font_style)
    ws_l.write_merge(0, 0, 9, 12, '勤',font_style)
    ws_l.write_merge(0, 0, 13, 16, '绩',font_style)
    ws_l.write_merge(0, 0, 17, 20, '廉',font_style)
    ws_l.write_merge(0, 0, 21, 23, '续聘意见',font_style)

    ws_m.write_merge(0, 0, 1, 4, '德',font_style)
    ws_m.write_merge(0, 0, 5, 8, '能',font_style)
    ws_m.write_merge(0, 0, 9, 12, '勤',font_style)
    ws_m.write_merge(0, 0, 13, 16, '绩',font_style)
    ws_m.write_merge(0, 0, 17, 20, '廉',font_style)
    ws_m.write_merge(0, 0, 21, 23, '续聘意见',font_style)

    ws_s.write_merge(0, 0, 1, 4, '德',font_style)
    ws_s.write_merge(0, 0, 5, 8, '能',font_style)
    ws_s.write_merge(0, 0, 9, 12, '勤',font_style)
    ws_s.write_merge(0, 0, 13, 16, '绩',font_style)
    ws_s.write_merge(0, 0, 17, 20, '廉',font_style)
    ws_s.write_merge(0, 0, 21, 23, '续聘意见',font_style)

    # Sheet body, remaining rows
    # font_style = xlwt.XFStyle()
    # 获取数据库数据
    rows = EmpAll.objects.all().values_list('obj', 'q11','q12','q13','q14','q21','q22','q23','q24','q31','q32',
                        'q33','q34','q41','q42','q43','q44','q51','q52','q53','q54','vA', 'vB','vC')
    rl = EmpLeader.objects.all().values_list('obj', 'q11','q12','q13','q14','q21','q22','q23','q24','q31','q32',
                        'q33','q34','q41','q42','q43','q44','q51','q52','q53','q54','vA', 'vB','vC')
    rm = EmpMiddle.objects.all().values_list('obj', 'q11','q12','q13','q14','q21','q22','q23','q24','q31','q32',
                        'q33','q34','q41','q42','q43','q44','q51','q52','q53','q54','vA', 'vB','vC')
    rs = EmpStaff.objects.all().values_list('obj', 'q11','q12','q13','q14','q21','q22','q23','q24','q31','q32',
                        'q33','q34','q41','q42','q43','q44','q51','q52','q53','q54','vA', 'vB','vC')
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
        count_all = EmpAll.objects.all()
        context = {
            'count_all':count_all,
        }
    return render(request,'employ/count/count_all.html',context)

def count_leader(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        count_leader = EmpLeader.objects.all()
        context = {
            'count_leader':count_leader,
        }
    return render(request,'employ/count/count_leader.html',context)

def count_middle(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        count_middle = EmpLeader.objects.all()
        context = {
            'count_middle':count_middle,
        }
    return render(request,'employ/count/count_middle.html',context=context)

def count_staff(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        count_staff = EmpStaff.objects.all()
        context = {
            'count_staff':count_staff,
        }
    return render(request,'employ/count/count_staff.html',context=context)