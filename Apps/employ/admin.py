from django.contrib import admin
from .models import *

#考评内容
class QConAdmin(admin.ModelAdmin):

    list_per_page = 50
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    search_fields = ('title',)
    list_display = ('title','detail')

admin.site.register(QContent,QConAdmin)

#续聘意见
class QOpAdmin(admin.ModelAdmin):

    list_per_page = 50
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    search_fields = ('title',)
    list_display = ('title',)

admin.site.register(QOpinion,QOpAdmin)

#测评对象
class EmpObjAdmin(admin.ModelAdmin):

    list_per_page = 50
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    fk_fields = ('grade','dep',)
    search_fields = ('obj',)
    list_display = ('obj',)

admin.site.register(EmpObject,EmpObjAdmin)

#干部考核表
class EmpPaperAdmin(admin.ModelAdmin):

    list_per_page = 50
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    search_fields = ('title','is_true')
    list_display = ('title','is_true','ctime')

admin.site.register(EmpPaper,EmpPaperAdmin)

#测评记录
class EmpRecordAdmin(admin.ModelAdmin):
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
    search_fields = ('paper','obj','user')
    list_display = ('paper','obj','q1','q2','q3','q4','q5','voted','grade','user')
    #控制list_display中的字段可以链接到对应对象的“更改”页面
    # list_display_links = ('paper', 'obj', 'dep','grade',)
admin.site.register(EmpRecord,EmpRecordAdmin)

