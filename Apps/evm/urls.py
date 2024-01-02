from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from evm import views

urlpatterns = [
    path('admin/', admin.site.urls),

    url(r'^login/', views.login, name='login'),  # 登录
    url(r'^register/', views.register, name='register'),  # 注册

    url(r'index/',views.index,name='index'),

    url(r'^user_list/',views.user_list,name='user_list'), #投票用户列表
    url(r'^create/', views.create, name='create'),  # 批量创建
    url(r'^upload/',views.upload,name='upload'), #批量导入用户
    url(r'^add_user/',views.add_user,name='add_user'), #新增用户
    url(r'^edit_user_detail/',views.edit_user_detail,name='edit_user_detail'),
    url(r'^edit_user/',views.edit_user,name='edit_user'), #编辑
    url(r'^drop_user/',views.drop_user,name='drop_user'), #删除
    url(r'^delete_users/',views.delete_users,name='delete_users'), #批量删除

    url(r'^grade_list/',views.grade_list,name='grade_list'), #角色列表
    url(r'^add_grade/',views.add_grade,name='add_grade'),
    url(r'^edit_detail/',views.edit_detail,name='edit_detail'),
    url(r'^edit_grade/',views.edit_grade,name='edit_grade'),
    url(r'^drop_grade/',views.drop_grade,name='drop_grade'),

    url(r'^dep_list/', views.dep_list, name='dep_list'),  # 部门列表
    url(r'^add_dep/', views.add_dep, name='add_dep'),
    url(r'^edit_dep_detail/', views.edit_dep_detail, name='edit_dep_detail'),
    url(r'^edit_dep/', views.edit_dep, name='edit_dep'),
    url(r'^drop_dep/', views.drop_dep, name='drop_dep'),

    # url(r'^ques1_list/', views.ques1_list, name='ques1_list'),  # 考评内容
    # url(r'^add_ques1/', views.add_ques1, name='add_ques1'),
    # url(r'^edit_ques1_detail/', views.edit_ques1_detail, name='edit_ques1_detail'),
    # url(r'^edit_ques1/', views.edit_ques1, name='edit_ques1'),
    # url(r'^drop_ques1/', views.drop_ques1, name='drop_ques1'),
    #
    # url(r'^ques2_list/', views.ques2_list, name='ques2_list'),  # 综合评价
    # url(r'^add_ques2/', views.add_ques2, name='add_ques2'),
    # url(r'^edit_ques2_detail/', views.edit_ques2_detail, name='edit_ques2_detail'),
    # url(r'^edit_ques2/', views.edit_ques2, name='edit_ques2'),
    # url(r'^drop_ques2/', views.drop_ques2, name='drop_ques2'),
    #
    # url(r'^obj_list/', views.obj_list, name='obj_list'),  # 测评对象
    # url(r'^add_obj/', views.add_obj, name='add_obj'),
    # url(r'^edit_obj_detail/', views.edit_obj_detail, name='edit_obj_detail'),
    # url(r'^edit_obj/', views.edit_obj, name='edit_obj'),
    # url(r'^drop_obj/', views.drop_obj, name='drop_obj'),
    # url(r'^delete_objs/',views.delete_objs,name='delete_objs'), #批量删除
    #
    # url(r'^paper_list/', views.paper_list, name='paper_list'),  # 综合评价
    # url(r'^add_paper/', views.add_paper, name='add_paper'),
    # url(r'^edit_paper_detail/', views.edit_paper_detail, name='edit_paper_detail'),
    # url(r'^edit_paper/', views.edit_paper, name='edit_paper'),
    # url(r'^drop_paper/', views.drop_paper, name='drop_paper'),
    #
    # url(r'^record_list/', views.record_list, name='record_list'),  # 测评记录
    #
    # url(r'^count/',views.count,name='count'), #测评统计
    # url(r'^count_all/',views.count_all,name='count_all'), #全体
    # url(r'^count_leader/',views.count_leader,name='count_leader'), #台领导
    # url(r'^count_middle/',views.count_middle,name='count_middle'), #中层干部
    # url(r'^count_staff/',views.count_staff,name='count_staff'), #普通职工
    # url(r'^download/',views.download,name='download'), #导出
    #
    #
    url(r'^logout/', views.logout, name='logout'), # 登出

]