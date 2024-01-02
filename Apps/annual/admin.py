from django.contrib import admin
from .models import *

class Q1Admin(admin.ModelAdmin):

    list_per_page = 50
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    search_fields = ('title',)
    list_display = ('title',)

admin.site.register(Question1,Q1Admin)

class Q2Admin(admin.ModelAdmin):

    list_per_page = 50
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    search_fields = ('title',)
    list_display = ('title',)

admin.site.register(Question2,Q2Admin)

class ObjAdmin(admin.ModelAdmin):

    list_per_page = 50
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    fk_fields = ('grade','dep',)
    search_fields = ('obj',)
    list_display = ('obj','grade','dep',)

admin.site.register(Object,ObjAdmin)

class PaperAdmin(admin.ModelAdmin):

    list_per_page = 50
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    search_fields = ('title','is_true')
    list_display = ('title','is_true','ctime','num')

admin.site.register(TestPaper,PaperAdmin)
class AnnRecordAdmin(admin.ModelAdmin):

    list_per_page = 50
    # ordering = ('-name',)
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    empty_value_display = ' -- '
    fk_fields = ('paper',)
    search_fields = ('obj','user')
    list_display = ('paper','obj','dep','score','voted','grade','user')
admin.site.register(AnnualRecord,AnnRecordAdmin)

class AnnualAllAdmin(admin.ModelAdmin):

    list_per_page = 50
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    empty_value_display = ' -- '
    search_fields = ('obj',)
    list_display = ('paper','obj','score','q1','q2','q3','q4','q5','q6','voted_A',
                    'voted_B','voted_C','voted_D','voted_E')

admin.site.register(AnnualAll,AnnualAllAdmin)

class AnnualLeaderAdmin(admin.ModelAdmin):

    list_per_page = 50
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    empty_value_display = ' -- '
    search_fields = ('obj',)
    list_display = ('paper','obj','score','q1','q2','q3','q4','q5','q6','voted_A',
                    'voted_B','voted_C','voted_D','voted_E')

admin.site.register(AnnualLeader,AnnualLeaderAdmin)

class AnnualMiddleAdmin(admin.ModelAdmin):

    list_per_page = 50
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    empty_value_display = ' -- '
    search_fields = ('obj',)
    list_display = ('paper','obj','score','q1','q2','q3','q4','q5','q6','voted_A',
                    'voted_B','voted_C','voted_D','voted_E')

admin.site.register(AnnualMiddle,AnnualMiddleAdmin)

class AnnualStaffAdmin(admin.ModelAdmin):

    list_per_page = 50
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    empty_value_display = ' -- '
    search_fields = ('obj',)
    list_display = ('paper','obj','score','q1','q2','q3','q4','q5','q6','voted_A',
                    'voted_B','voted_C','voted_D','voted_E')

admin.site.register(AnnualStaff,AnnualStaffAdmin)
