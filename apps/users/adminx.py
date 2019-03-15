
import xadmin
from xadmin import views   #导入xadmin中的views,用于和 BaseSettings类绑定
from xadmin.plugins.auth import UserAdmin   #导入xadmin中的UserAdmin


from .models import EmailVerifyRecord
from .models import Banner
from .models import UserProfile


class EmailVerifyRecordAdmin(object):
    diduan = ['code','email','send_type','send_time']
    # list_display = ['code','email','send_type','send_time']   #定义显示的字段
    # search_fields = ['code','email','send_type','send_time']   #定义搜索的字段
    # list_filter = ['code','email','send_type','send_time']   #定义筛选的字段
    list_display = diduan   #定义显示的字段
    search_fields = diduan   #定义搜索的字段
    list_filter = diduan   #定义筛选的字段
    model_icon = 'fa fa-address-book-o'  #定义图标显示

xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)


class BannerAdmin(object):
    diduan = ['title', 'image', 'url', 'index', 'add_time']
    list_display = diduan   #定义显示的字段
    search_fields = diduan   #定义搜索的字段
    list_filter = diduan   #定义筛选的字段

xadmin.site.register(Banner, BannerAdmin)


class BaseSettings(object):   #全站的配置类, 配置主题
    enable_themes = True  #主题功能,enable_themes=True 表示要使用它的主题功能，xadmin默认是取消掉的
    use_bootswatch = True   #xadmin默认是取消掉的

xadmin.site.register(views.BaseAdminView, BaseSettings)   #注册BaseSettings

class GlobalSettings(object):   ##全站的配置类
    site_title = "慕学后台管理系统"   #页面左上角的标题名称
    site_footer = "慕学在线网"   #页面底部的文字显示内容
    menu_style = "accordion"  # 将一个app下的内容收起来

xadmin.site.register(views.CommAdminView, GlobalSettings)   #注册GlobalSettings



class UserProfileAdmin(UserAdmin):
    def get_form_layout(self):   #重载UserAdmin中的get_form_layout方法来自定义xadmin中用户信息页面
        if self.org_obj:
            self.form_layout = (
                Main(
                    Fieldset('',     #对应用户名和密码区域
                             'username', 'password',
                             css_class='unsort no_title'
                             ),
                    Fieldset(_('Personal info'),   #对应个人信息区域
                             Row('first_name', 'last_name'),
                             'email'
                             ),
                    Fieldset(_('Permissions'),   #对应权限区域
                             'groups', 'user_permissions'
                             ),
                    Fieldset(_('Important dates'),   #对应重要日期区域
                             'last_login', 'date_joined'
                             ),
                ),
                Side(   #对应状态区域
                    Fieldset(_('Status'),
                             'is_active', 'is_staff', 'is_superuser',
                             ),
                )
            )
        return super(UserAdmin, self).get_form_layout()
#
# xadmin.site.register(UserProfile, UserProfileAdmin)   #注册UserProfile

# from django.contrib.auth.models import User
# xadmin.site.unregister(User)   #卸载掉User模块