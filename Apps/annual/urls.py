from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from annual import views

urlpatterns = [
    path('admin/', admin.site.urls),

    url(r'^login/', views.login, name='login'),  # 登录
    url(r'^index/', views.index, name='index'),  # 首页
    url(r'^detail',views.detail,name='detail'), # 测评列表
    url(r'^startVote',views.startVote,name='startVote'), #开始投票
    url(r'^voteCount/', views.voteCount, name='voteCount'),  # 提交
    url(r'^logout/', views.logout, name='logout'), # 登出

    url(r'^ques1_list/', views.ques1_list, name='ques1_list'),  # 考评内容
    url(r'^add_ques1/', views.add_ques1, name='add_ques1'),
    url(r'^edit_ques1_detail/', views.edit_ques1_detail, name='edit_ques1_detail'),
    url(r'^edit_ques1/', views.edit_ques1, name='edit_ques1'),
    url(r'^drop_ques1/', views.drop_ques1, name='drop_ques1'),

    url(r'^ques2_list/', views.ques2_list, name='ques2_list'),  # 综合评价
    url(r'^add_ques2/', views.add_ques2, name='add_ques2'),
    url(r'^edit_ques2_detail/', views.edit_ques2_detail, name='edit_ques2_detail'),
    url(r'^edit_ques2/', views.edit_ques2, name='edit_ques2'),
    url(r'^drop_ques2/', views.drop_ques2, name='drop_ques2'),

    url(r'^obj_list/', views.obj_list, name='obj_list'),  # 测评对象
    url(r'^add_obj/', views.add_obj, name='add_obj'),
    url(r'^edit_obj_detail/', views.edit_obj_detail, name='edit_obj_detail'),
    url(r'^edit_obj/', views.edit_obj, name='edit_obj'),
    url(r'^drop_obj/', views.drop_obj, name='drop_obj'),
    url(r'^delete_objs/',views.delete_objs,name='delete_objs'), #批量删除

    url(r'^paper_list/', views.paper_list, name='paper_list'),  # 综合评价
    url(r'^add_paper/', views.add_paper, name='add_paper'),
    url(r'^edit_paper_detail/', views.edit_paper_detail, name='edit_paper_detail'),
    url(r'^edit_paper/', views.edit_paper, name='edit_paper'),
    url(r'^drop_paper/', views.drop_paper, name='drop_paper'),

    url(r'^record_list/', views.record_list, name='record_list'),  # 测评记录

    url(r'^count/',views.count,name='count'), #测评统计
    url(r'^count_all/',views.count_all,name='count_all'), #全体
    url(r'^count_leader/',views.count_leader,name='count_leader'), #台领导
    url(r'^count_middle/',views.count_middle,name='count_middle'), #中层干部
    url(r'^count_staff/',views.count_staff,name='count_staff'), #普通职工
    url(r'^download/',views.download,name='download'), #导出


]