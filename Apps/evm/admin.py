from django.contrib import admin
#最上面增加import
from django.contrib.admin.models import LogEntry

from .models import *

admin.site.site_header = '测评投票系统后台'
admin.site.site_title = '测评投票系统'


#角色
class GradeAdmin(admin.ModelAdmin):

    list_per_page = 50
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    search_fields = ('grade',)
    list_display = ('grade','weight')

admin.site.register(Grade,GradeAdmin)

#部门
class DepAdmin(admin.ModelAdmin):

    list_per_page = 50
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    search_fields = ('dep',)
    list_display = ('dep',)

admin.site.register(Department,DepAdmin)

#用户
class UserAdmin(admin.ModelAdmin):

    list_per_page = 50
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    empty_value_display = ' -- '
    search_fields = ('name',)
    list_display = ('name','dep','grade','is_true','password')
    list_display_links = ('name','dep','grade',)

admin.site.register(User,UserAdmin)

class AdminUserAdmin(admin.ModelAdmin):

    list_display = ('name','password')

admin.site.register(AdminUser,AdminUserAdmin)




