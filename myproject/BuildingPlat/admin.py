from django.contrib import admin
from .models import CallBid,WinBid

# Register your models here.
class CallBidAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        """函数作用：使当前登录的用户只能看到自己负责的服务器"""
        qs = super(CallBidAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('name', 'district', 'type', 'purl', 'tenderee','tenderer',\
                    'address', 'docnmb', 'startaffich','endaffich','endRegistration')

    # 筛选器
    list_filter = ('district', 'dom')
    search_fields = ('name', 'district', )  # 搜索字段
    #list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 25
    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ('name',)
    # # 详细时间分层筛选
    date_hierarchy = 'startaffich'
    # purl = admin.widget.


class WinBidAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        """函数作用：使当前登录的用户只能看到自己负责的服务器"""
        qs = super(WinBidAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('name', 'district', 'type', 'purl','winner',\
                    'address', 'docnmb', 'startaffich','endaffich')

    # 筛选器
    list_filter = ('district', 'dom')
    search_fields = ('name', 'district', )  # 搜索字段
    #list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 25
    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ('name',)
    # # 详细时间分层筛选
    date_hierarchy = 'startaffich'
    # purl = admin.widget.

admin.site.site_header = '建筑信息智慧平台管理'#首页>建筑信息>招标信息django
admin.site.site_title = '建筑信息智慧平台管理'#登录
admin.site.register(CallBid,CallBidAdmin)
admin.site.register(WinBid,WinBidAdmin)

