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
from .forms import *
import json
from django.urls import reverse
from .models import *

def login(request):
    if request.session.get('is_login', None):
        return HttpResponseRedirect(reverse('annual:index', args=()))
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
                    return render(request,'annual/login/login.html',locals())
            except:
                msg = '用户不存在！'
                return render(request, 'annual/login/login.html', locals())
            if user.password == password:
                request.session['is_login'] = True
                request.session['username'] = user.name
                return HttpResponseRedirect(reverse('annual:index', args=()))
            else:
                msg = '密码不正确！'
                return render(request, 'annual/login/login.html', locals())
        else:
            return render(request, 'annual/login/login.html', locals())

    login_form = UserForm()
    return render(request, 'annual/login/login.html', locals())

def index(request):
    if not request.session.get('is_login', None):
        return HttpResponseRedirect(reverse('annual:login', args=()))
    else:
        username = request.session.get('username', None)
        user = User.objects.get(name=username)
        paper = TestPaper.objects.filter(is_true=True)

        context = {
            'user': user,
            'paper': paper,
        }
    return render(request, 'annual/voting/index.html', context=context)

def detail(request):
    if not request.session.get('is_login',None):
        return HttpResponseRedirect(reverse('annual:login', args=()))
    else:
        username = request.GET.get('name')
        id = request.GET.get('id')
        paper = TestPaper.objects.filter(id=id)

        context = {
            'user': username,
            'id' : id,
            'paper': paper,
        }
    return render(request,'annual/voting/detail.html',context)

def startVote(request):
    if not request.session.get('is_login',None):
        return HttpResponseRedirect(reverse('annual:login', args=()))
    else:
        username = request.GET.get('name')
        id = request.GET.get('id')
        obj = request.GET.get('obj')
        user = User.objects.get(name=username)
        paper = Object.objects.filter(obj=obj)

        num = TestPaper.objects.filter(id=id).values('num')
        yx_num = num[0]['num']
        is_num = AnnualRecord.objects.filter(paper_id=id, user=user, voted='优秀').count()
        num = yx_num - is_num

        context = {
            'user':user,
            'id':id,
            'paper':paper,
            'obj':obj,
            'num':num
        }
    return render(request,'annual/voting/vote.html',context=context)

def voteCount(request):

    if request.method == 'POST':
        user = request.POST.get('name')
        obj = request.POST.get('obj')
        id = request.POST.get('id')

        num = TestPaper.objects.filter(id=id).values('num')
        yx_num = num[0]['num']
        grade = User.objects.filter(name=user).values('grade')
        g = grade[0]['grade']

        t = timezone.now()
        now = t.strftime("%Y-%m-%d %H:%M:%S")

        ques1 = Object.objects.filter(obj=obj).values("pid1").values('pid1__title')

        ques2 = Object.objects.filter(obj=obj).values("pid2").values('pid2__title')
        qid = ques2[0]['pid2__title']
        voted2 = request.POST.get(qid)

        if voted2 is None:
            msg = '请返回进行综合评价！'
            return render(request, 'annual/voting/error.html', {"msg": msg})
        else:
            score = 0
            list = []
            for p in ques1:
                qid = str(p['pid1__title'])
                vote = request.POST.get(qid)
                if vote is None:
                    msg = "请对所有问题打分！"
                    return render(request, 'annual/voting/error.html', {"msg": msg})
                else:
                    voted = int(vote)
                    data = (qid,voted)
                    list.append(data)
                    score += voted
        dic = dict(list)
        de = dic['德']
        neng = dic['能']
        qin = dic['勤']
        ji = dic['绩']
        xue = dic['学']
        lian = dic['廉']
        # 优秀个数
        is_num = AnnualRecord.objects.filter(paper_id=id, user=user, voted='优秀').count()
        if is_num < yx_num:
            AnnualRecord.objects.filter(paper_id=id, obj=obj, user=user).delete()
            AnnualRecord.objects.create(user=user, score=score, voted=voted2, paper_id=id, obj=obj,
                                  grade=g, time=now,q1=de,q2=neng,q3=qin,q4=ji,q5=xue,q6=lian)
        else:
            if voted2 == '优秀':
                record = AnnualRecord.objects.filter(paper_id=id, obj=obj, user=user, voted='优秀')
                if record:
                    AnnualRecord.objects.filter(paper_id=id, obj=obj, user=user).delete()
                    AnnualRecord.objects.create(user=user, score=score, voted=voted2, paper_id=id, obj=obj,
                                                 grade=g, time=now,q1=de,q2=neng,q3=qin,q4=ji,q5=xue,q6=lian)
                else:
                    msg = "优秀人数已达上限！"
                    return render(request, 'annual/voting/error.html', {"msg": msg})
            else:
                AnnualRecord.objects.filter(paper_id=id, obj=obj, user=user).delete()
                AnnualRecord.objects.create(user=user, score=score, voted=voted2, paper_id=id, obj=obj,
                                             grade=g, time=now,q1=de,q2=neng,q3=qin,q4=ji,q5=xue,q6=lian)
        paper = TestPaper.objects.filter(id=id)
        pobjs = paper.values('obj__obj')
        pobj = []
        for obj in pobjs:
            p = obj['obj__obj']

            pobj.append(p)

        robjs = AnnualRecord.objects.filter(paper_id=id, user=user).values('obj')
        robj = []

        for obj in robjs:
            r = obj['obj']
            robj.append(r)

        pobj.sort()
        robj.sort()
        if robj == pobj:
            User.objects.filter(name=user).update(is_true=False)

            time.sleep(1)
            request.session.flush()
            return HttpResponseRedirect(reverse('annual:login', args=()))
        else:
            username = request.session.get('username', None)
            user = User.objects.get(name=username)
            paper = TestPaper.objects.filter(is_true=True)
            context = {
                'user': user,
                'paper': paper,
            }

            return render(request, 'annual/voting/detail.html', context=context)

def logout(request):
    if not request.session.get('is_login', None):
        return HttpResponseRedirect(reverse('annual:login', args=()))
    else:
        username = request.session.get('username', None)
        user = User.objects.get(name=username)
        paper = TestPaper.objects.filter(is_true=True)
        for p in paper:
            for o in p.obj.all():
                if AnnualRecord.objects.filter(obj=o, user=user).exists():
                    pass
                else:
                    return JsonResponse({"code": 1, "msg": o.obj})
        User.objects.filter(name=user).update(is_true=False)
        request.session.flush()
        return JsonResponse({"code": 0})

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

def ques1_list(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        queryset = Question1.objects.all()
        form = Q1ModelForm
        context = {
            'ques1_list': queryset,
            'form': form,
        }
    return render(request, 'annual/ques1_list.html', context)

@csrf_exempt
def add_ques1(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        form = Q1ModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            data_dict = {'status': True}
            return HttpResponse(json.dumps(data_dict))
        data_dict = {'status': False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))

def edit_ques1_detail(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        uid = request.GET.get("uid")
        exists =Question1.objects.filter(id=uid).exists()
        if not exists:
            return HttpResponse(json.dumps({'status': False, 'error': "数据不存在"}))
        row_dict = Question1.objects.filter(id=uid).values('title','a','b','c','d','e','f','g','h','i','j').first()
    return HttpResponse(json.dumps({'status': True, 'data': row_dict}))

@csrf_exempt
def edit_ques1(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        uid = request.GET.get("uid")
        row_object = Question1.objects.filter(id=uid).first()
        if not row_object:
            return HttpResponse(json.dumps({'status': False, 'error_total': "数据不存在"}))
        form = Q1ModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            data_dict = {'status': True}
            return HttpResponse(json.dumps(data_dict))
        data_dict = {'status': False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))

def drop_ques1(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        uid = request.GET.get("uid")
        exists = Question1.objects.filter(id=uid).exists()

        if not exists:
            return HttpResponse(json.dumps({'status': False, 'error': "数据不存在"}))
        Question1.objects.filter(id=uid).delete()
    return HttpResponse(json.dumps({'status': True}))

def ques2_list(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        queryset = Question2.objects.all()
        form = Q2ModelForm
        context = {
            'ques2_list': queryset,
            'form': form,
        }
    return render(request, 'annual/ques2_list.html', context)

@csrf_exempt
def add_ques2(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        form = Q2ModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            data_dict = {'status': True}
            return HttpResponse(json.dumps(data_dict))
        data_dict = {'status': False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))

def edit_ques2_detail(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        uid = request.GET.get("uid")
        exists =Question2.objects.filter(id=uid).exists()
        if not exists:
            return HttpResponse(json.dumps({'status': False, 'error': "数据不存在"}))
        row_dict = Question2.objects.filter(id=uid).values('title','a','b','c','d','e').first()
    return HttpResponse(json.dumps({'status': True, 'data': row_dict}))

@csrf_exempt
def edit_ques2(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        uid = request.GET.get("uid")
        row_object = Question2.objects.filter(id=uid).first()
        if not row_object:
            return HttpResponse(json.dumps({'status': False, 'error_total': "数据不存在"}))
        form = Q2ModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            data_dict = {'status': True}
            return HttpResponse(json.dumps(data_dict))
        data_dict = {'status': False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))

def drop_ques2(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        uid = request.GET.get("uid")
        exists = Question2.objects.filter(id=uid).exists()

        if not exists:
            return HttpResponse(json.dumps({'status': False, 'error': "数据不存在"}))
        Question2.objects.filter(id=uid).delete()
    return HttpResponse(json.dumps({'status': True}))

def obj_list(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        queryset = Object.objects.all()
        form = ObjModelForm
        context = {
            'obj_list': queryset,
            'form': form,
        }
    return render(request, 'annual/obj_list.html', context)

@csrf_exempt
def add_obj(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        form = ObjModelForm(data=request.POST)
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
        exists =Object.objects.filter(id=uid).exists()
        if not exists:
            return HttpResponse(json.dumps({'status': False, 'error': "数据不存在"}))
        row_dict = Object.objects.filter(id=uid).values('obj','dep','grade','pid1','pid2').first()
    return HttpResponse(json.dumps({'status': True, 'data': row_dict}))

@csrf_exempt
def edit_obj(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        uid = request.GET.get("uid")
        row_object = Object.objects.filter(id=uid).first()
        if not row_object:
            return HttpResponse(json.dumps({'status': False, 'error_total': "数据不存在"}))
        form = ObjModelForm(data=request.POST, instance=row_object)
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
        exists = Object.objects.filter(id=uid).exists()

        if not exists:
            return HttpResponse(json.dumps({'status': False, 'error': "数据不存在"}))
        Object.objects.filter(id=uid).delete()
    return HttpResponse(json.dumps({'status': True}))

def delete_objs(request):
    if request.method == 'POST':
        values = request.POST.getlist('vals')
        for i in values:
            if i != '':
                drop_obj = Object.objects.get(id=i)
                drop_obj.delete()
        return HttpResponseRedirect(reverse('annual:obj_list', args=()))

def paper_list(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        queryset = TestPaper.objects.all()
        form = PaperModelForm
        context = {
            'paper_list': queryset,
            'form': form,
        }
    return render(request, 'annual/paper_list.html', context)

@csrf_exempt
def add_paper(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        form = PaperModelForm(data=request.POST)
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
        exists =TestPaper.objects.filter(id=uid).exists()
        if not exists:
            return HttpResponse(json.dumps({'status': False, 'error': "数据不存在"}))
        row_dict = TestPaper.objects.filter(id=uid).values('title','obj','is_true','num').first()
    return HttpResponse(json.dumps({'status': True, 'data': row_dict},cls=ComplexEncoder))

@csrf_exempt
def edit_paper(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        uid = request.GET.get("uid")
        row_object = TestPaper.objects.filter(id=uid).first()
        if not row_object:
            return HttpResponse(json.dumps({'status': False, 'error_total': "数据不存在"}))
        form = PaperModelForm(data=request.POST, instance=row_object)
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
        exists = TestPaper.objects.filter(id=uid).exists()

        if not exists:
            return HttpResponse(json.dumps({'status': False, 'error': "数据不存在"}))
        TestPaper.objects.filter(id=uid).delete()
    return HttpResponse(json.dumps({'status': True}))

def record_list(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        id = request.GET.get('id')
        queryset = AnnualRecord.objects.filter(paper_id=id)
        form = RecordModelForm
        context = {
            'record_list': queryset,
            'form': form,
        }
    return render(request, 'annual/record_list.html', context)

def count(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        id = request.GET.get('id')
        objs = TestPaper.objects.filter(id=id).values('obj__obj')

        AnnualAll.objects.all().delete()
        AnnualLeader.objects.all().delete()
        AnnualMiddle.objects.all().delete()
        AnnualStaff.objects.all().delete()
        for obj in objs:
            obj = obj['obj__obj']
            records = AnnualRecord.objects.filter(paper_id=id,obj=obj).values(
                'score','q1','q2','q3','q4','q5','q6')
            score = 0
            q1 = 0
            q2 = 0
            q3 = 0
            q4 = 0
            q5 = 0
            q6 = 0
            for record in records:
                s = int(record['score'])
                s1 = int(record['q1'])
                s2 = int(record['q2'])
                s3 = int(record['q3'])
                s4 = int(record['q4'])
                s5 = int(record['q5'])
                s6 = int(record['q6'])
                score += s
                q1 += s1
                q2 += s2
                q3 += s3
                q4 += s4
                q5 += s5
                q6 += s6
            v1 = AnnualRecord.objects.filter(paper_id=id,obj=obj,voted='优秀').count()
            v2 = AnnualRecord.objects.filter(paper_id=id,obj=obj,voted='合格').count()
            v3 = AnnualRecord.objects.filter(paper_id=id,obj=obj,voted='基本合格').count()
            v4 = AnnualRecord.objects.filter(paper_id=id,obj=obj,voted='不合格').count()
            v5 = AnnualRecord.objects.filter(paper_id=id,obj=obj,voted='弃权').count()
            AnnualAll.objects.filter(paper=id,obj=obj).delete()
            AnnualAll.objects.create(paper=id,obj=obj,score=score,q1=q1,q2=q2,q3=q3,q4=q4,q5=q5,q6=q6,
                                    voted_A=v1,voted_B=v2,voted_C=v3,voted_D=v4,voted_E=v5)
            s_l = 0
            lq1 = 0
            lq2 = 0
            lq3 = 0
            lq4 = 0
            lq5 = 0
            lq6 = 0
            r_l = AnnualRecord.objects.filter(paper_id=id,obj=obj,grade='台领导').values(
                'score','q1','q2','q3','q4','q5','q6')
            for r in r_l:
                s = int(r['score'])
                ls1 = int(r['q1'])
                ls2 = int(r['q2'])
                ls3 = int(r['q3'])
                ls4 = int(r['q4'])
                ls5 = int(r['q5'])
                ls6 = int(r['q6'])
                s_l += s
                lq1 += ls1
                lq2 += ls2
                lq3 += ls3
                lq4 += ls4
                lq5 += ls5
                lq6 += ls6

            v11 = AnnualRecord.objects.filter(paper_id=id,obj=obj,voted='优秀',grade='台领导').count()
            v12 = AnnualRecord.objects.filter(paper_id=id,obj=obj,voted='合格',grade='台领导').count()
            v13 = AnnualRecord.objects.filter(paper_id=id,obj=obj,voted='基本合格',grade='台领导').count()
            v14 = AnnualRecord.objects.filter(paper_id=id,obj=obj,voted='不合格',grade='台领导').count()
            v15 = AnnualRecord.objects.filter(paper_id=id,obj=obj,voted='弃权',grade='台领导').count()

            AnnualLeader.objects.filter(paper=id,obj=obj).delete()
            AnnualLeader.objects.create(paper=id,obj=obj,score=s_l,q1=lq1,q2=lq2,q3=lq3,q4=lq4,q5=lq5,q6=lq6,
                                       voted_A=v11,voted_B=v12, voted_C=v13, voted_D=v14, voted_E=v15)
            s_m = 0
            mq1 = 0
            mq2 = 0
            mq3 = 0
            mq4 = 0
            mq5 = 0
            mq6 = 0
            r_m = AnnualRecord.objects.filter(paper_id=id,obj=obj,grade='中层干部').values(
                'score','q1','q2','q3','q4','q5','q6')
            for r in r_m:
                s = int(r['score'])
                ms1 = int(r['q1'])
                ms2 = int(r['q2'])
                ms3 = int(r['q3'])
                ms4 = int(r['q4'])
                ms5 = int(r['q5'])
                ms6 = int(r['q6'])
                s_m += s
                mq1 += ms1
                mq2 += ms2
                mq3 += ms3
                mq4 += ms4
                mq5 += ms5
                mq6 += ms6
            v21 = AnnualRecord.objects.filter(paper_id=id, obj=obj, voted='优秀', grade='中层干部').count()
            v22 = AnnualRecord.objects.filter(paper_id=id, obj=obj, voted='合格', grade='中层干部').count()
            v23 = AnnualRecord.objects.filter(paper_id=id, obj=obj, voted='基本合格', grade='中层干部').count()
            v24 = AnnualRecord.objects.filter(paper_id=id, obj=obj, voted='不合格', grade='中层干部').count()
            v25 = AnnualRecord.objects.filter(paper_id=id, obj=obj, voted='弃权', grade='中层干部').count()

            AnnualMiddle.objects.filter(paper=id, obj=obj).delete()
            AnnualMiddle.objects.create(paper=id, obj=obj, score=s_m,q1=mq1,q2=mq2,q3=mq3,q4=mq4,q5=mq5,q6=mq6,
                                       voted_A=v21,voted_B=v22, voted_C=v23, voted_D=v24, voted_E=v25)

            s_s = 0
            sq1 = 0
            sq2 = 0
            sq3 = 0
            sq4 = 0
            sq5 = 0
            sq6 = 0
            r_s = AnnualRecord.objects.filter(paper_id=id,obj=obj,grade='普通职工').values(
                'score','q1','q2','q3','q4','q5','q6')
            for r in r_s:
                s = int(r['score'])
                ss1 = int(r['q1'])
                ss2 = int(r['q2'])
                ss3 = int(r['q3'])
                ss4 = int(r['q4'])
                ss5 = int(r['q5'])
                ss6 = int(r['q6'])
                s_s += s
                sq1 += ss1
                sq2 += ss2
                sq3 += ss3
                sq4 += ss4
                sq5 += ss5
                sq6 += ss6
            v31 = AnnualRecord.objects.filter(paper_id=id, obj=obj, voted='优秀', grade='普通职工').count()
            v32 = AnnualRecord.objects.filter(paper_id=id, obj=obj, voted='合格', grade='普通职工').count()
            v33 = AnnualRecord.objects.filter(paper_id=id, obj=obj, voted='基本合格', grade='普通职工').count()
            v34 = AnnualRecord.objects.filter(paper_id=id, obj=obj, voted='不合格', grade='普通职工').count()
            v35 = AnnualRecord.objects.filter(paper_id=id, obj=obj, voted='弃权', grade='普通职工').count()

            AnnualStaff.objects.filter(paper=id, obj=obj).delete()
            AnnualStaff.objects.create(paper=id,obj=obj,score=s_s,q1=sq1,q2=sq2,q3=sq3,q4=sq4,q5=sq5,q6=sq6,
                                      voted_A=v31, voted_B=v32, voted_C=v33, voted_D=v34, voted_E=v35)

    count = AnnualAll.objects.all()
    context = {
        'count':count,
    }
    return render(request,'annual/count/count.html',context=context)

def download(request):
    t = timezone.now()
    date = t.strftime("%Y%m%d")

    paper_id = AnnualAll.objects.all().values('paper')
    id = paper_id[0]['paper']
    title = TestPaper.objects.filter(id=id).values('title')
    name = title[0]['title']

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = "attachment; filename={0}_{1}.xls".format(escape_uri_path(name),date)
    wb = xlwt.Workbook(encoding='utf-8')

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
    font_style.font.bold = True
    columns = ['测评对象','总分','德','能','勤','绩','学','廉','优秀','合格','基本合格','不合格','弃权']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
        ws_l.write(rl_num, col_num, columns[col_num], font_style)
        ws_m.write(rm_num, col_num, columns[col_num], font_style)
        ws_s.write(rs_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = AnnualAll.objects.all().values_list('obj', 'score', 'q1','q2','q3','q4','q5','q6',
                                              'voted_A', 'voted_B','voted_C','voted_D','voted_E')
    rl = AnnualLeader.objects.all().values_list('obj', 'score', 'q1','q2','q3','q4','q5','q6',
                                               'voted_A', 'voted_B','voted_C','voted_D','voted_E')
    rm = AnnualMiddle.objects.all().values_list('obj', 'score', 'q1','q2','q3','q4','q5','q6',
                                               'voted_A', 'voted_B','voted_C','voted_D','voted_E')
    rs = AnnualStaff.objects.all().values_list('obj', 'score', 'q1','q2','q3','q4','q5','q6',
                                              'voted_A', 'voted_B','voted_C','voted_D','voted_E')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    for row in rl:
        rl_num += 1
        for col_num in range(len(row)):
            ws_l.write(rl_num, col_num, row[col_num], font_style)
    for row in rm:
        rm_num += 1
        for col_num in range(len(row)):
            ws_m.write(rm_num, col_num, row[col_num], font_style)
    for row in rs:
        rs_num += 1
        for col_num in range(len(row)):
            ws_s.write(rs_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response

def count_all(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        count_all = AnnualAll.objects.all()
        context = {
            'count_all':count_all,
        }
    return render(request,'annual/count/count_all.html',context)

def count_leader(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        count_leader = AnnualLeader.objects.all()
        context = {
            'count_leader':count_leader,
        }
    return render(request,'annual/count/count_leader.html',context)

def count_middle(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        count_middle = AnnualMiddle.objects.all()
        context = {
            'count_middle':count_middle,
        }
    return render(request,'annual/count/count_middle.html',context=context)

def count_staff(request):
    if not request.session.get('admin_login', None):
        return HttpResponseRedirect(reverse('evm:login', args=()))
    else:
        count_staff = AnnualStaff.objects.all()
        context = {
            'count_staff':count_staff,
        }
    return render(request,'annual/count/count_staff.html',context=context)
