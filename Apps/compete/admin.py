from django.contrib import admin
from .models import *

class PostAdmin(admin.ModelAdmin):
    list_per_page = 50
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    search_fields = ('post',)
    list_display = ('post','num')

admin.site.register(Post, PostAdmin)

class QuseObjAdmin(admin.ModelAdmin):
    list_per_page = 50
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    search_fields = ('post',)
    list_display = ('obj','post','a','b','c')

admin.site.register(QuesObj, QuseObjAdmin)

#干部考核表
class CompPaperAdmin(admin.ModelAdmin):

    list_per_page = 50
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    search_fields = ('title','is_true')
    list_display = ('title','is_true','ctime')

admin.site.register(Paper,CompPaperAdmin)

#测评记录
class CompRecordAdmin(admin.ModelAdmin):

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50
    # ordering设置默认排序字段，负号表示降序排序
    # ordering = ('-name',)
    # 操作项功能显示位置设置，两个都为True则顶部和底部都显示
    actions_on_top = True
    actions_on_bottom = True
    # 操作项功能显示选中项的数目
    actions_selection_counter = True
    # 字段为空值显示的内容
    empty_value_display = ' -- '
    # fk_fields 设置显示外键字段
    fk_fields = ('paper',)
    # 搜索功能及能实现搜索的字段
    search_fields = ('obj','user')
    list_display = ('paper','obj','voted','grade','user')
    #控制list_display中的字段可以链接到对应对象的“更改”页面
    # list_display_links = ('paper', 'obj', 'dep','grade',)
admin.site.register(CompRecord,CompRecordAdmin)

#测评统计/全体
class CompAllAdmin(admin.ModelAdmin):

    list_per_page = 50
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    empty_value_display = ' -- '
    search_fields = ('obj',)
    list_display = ('paper','obj','post','num','vA', 'vB','vC')

admin.site.register(CompAll,CompAllAdmin)

#测评统计/台领导
class CompLeaderAdmin(admin.ModelAdmin):

    list_per_page = 50
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    empty_value_display = ' -- '
    search_fields = ('obj',)
    list_display = ('paper','obj','post','num','vA', 'vB','vC')

admin.site.register(CompLeader,CompLeaderAdmin)

#测评统计/中层干部
class CompMiddleAdmin(admin.ModelAdmin):

    list_per_page = 50
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    empty_value_display = ' -- '
    search_fields = ('obj',)
    list_display = ('paper','obj','post','num','vA', 'vB','vC')

admin.site.register(CompMiddle,CompMiddleAdmin)

#测评统计/普通职工
class CompStaffAdmin(admin.ModelAdmin):

    list_per_page = 50
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    empty_value_display = ' -- '
    search_fields = ('obj',)
    list_display = ('paper','obj','post','num','vA', 'vB','vC')

admin.site.register(CompStaff,CompStaffAdmin)