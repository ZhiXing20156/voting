from django.contrib import admin
from .models import *

class RankAdmin(admin.ModelAdmin):
    list_per_page = 50
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    search_fields = ('rank',)
    list_display = ('rank',)

admin.site.register(Rank, RankAdmin)

class ReObjAdmin(admin.ModelAdmin):
    list_per_page = 50
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    search_fields = ('obj',)
    list_display = ('obj','sex','birth','age','work_time','dates','status','post','time_in_post','job_title',
                    'degree','remark')

admin.site.register(ReObj, ReObjAdmin)

#民主推荐表
class RePaperAdmin(admin.ModelAdmin):

    list_per_page = 50
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    search_fields = ('title','is_true')
    list_display = ('title','post','num','is_true','c_time')

admin.site.register(RePaper,RePaperAdmin)

#测评记录
class ReRecordAdmin(admin.ModelAdmin):

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
    list_display = ('paper','obj','grade','user')
    #控制list_display中的字段可以链接到对应对象的“更改”页面
    # list_display_links = ('paper', 'obj', 'dep','grade',)
admin.site.register(ReRecord,ReRecordAdmin)

#测评统计/
class ReCountAdmin(admin.ModelAdmin):

    list_per_page = 50
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    empty_value_display = ' -- '

    list_display = ('paper','obj','post','vote','ratio')

admin.site.register(ReCount,ReCountAdmin)
