"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.urls import reverse   #导入xadmin所需要的reverse包
from django.views.generic import TemplateView   #导入django处理静态文件的包TemplateView
import xadmin   #导入xadmin包
import captcha   #导入captcha包
from django.views.static import serve   #导入django处理静态文件的包serve ,用于处理midia路径下的文件

# from users.views import user_login
from users.views import LoginView   #导入LoginView类
from users.views import RegisterView   #导入RegisterView类
from users.views import ActiveUserView  #导入ActiveUserView类
from users.views import ForgetPwdView #导入ForgetPwdView类
from users.views import ResetView #导入ResetView类
from users.views import ModifyPwdView #导入ModifyPwdView类
from organization.views import OrgView   #导入OrgView类
from .settings import MEDIA_ROOT    #导入Settings中配置的MEDIA_ROOT

urlpatterns = [
    path('xadmin/', xadmin.site.urls),   #admin换成xadmin
    path('index/', TemplateView.as_view(template_name="index.html"), name="index"),
    # path('login/', user_login, name="login"),   #login()是调用这个函数，login是指向这个函数
    # path('usercenter-info/', login, name="usercenter-info"),   #login()是调用这个函数，login是指向这个函数
    path('login/', LoginView.as_view(), name="login"),   #调用as_view()方法，不是传这个方法的句柄出来
    path('register/', RegisterView.as_view(), name="register"),   #调用as_view()方法，不是传这个方法的句柄出来
    path('captcha/', include('captcha.urls')),   #配置captcha路径
    path('active/<path:active_code>/',ActiveUserView.as_view(), name="user_active"),   #url中提取一个变量当作参数，?P:表示要提取一个变量当作参数
                                                                    #<>:尖括号里的字段任意命名
                                                                    #.*:正则表达式，表示把active后面的东西全部取出来，并放到active_code参数中
                                                                    #/：表示路径
    path('forget/', ForgetPwdView.as_view(), name="forget_pwd"),   #配置忘记密码页面的访问路径
    path('reset/<path:active_code>/',ResetView.as_view(), name="reset_pwd"),    #配置点击重置密码邮箱链接的路径
    path('modify_pwd/', ModifyPwdView.as_view(), name="modify_pwd"),  # 配置修改密码页面的访问路径

    #课程机构首页
    # path('org_list/', OrgView.as_view(), name="org_list"),  # 配置课程列表页面的访问路径
    #课程机构url配置
    path('org/', include('organization.urls', namespace='org')),   #配置课程机构url,namespace指明命名空间，用命名空间做限定

    #配置上传文件的访问处理函数
    path('media/<path:path>',serve, {"document_root":MEDIA_ROOT}),    #配置处理引用midia路径下文件的路径,调用serve方法,需要传入参数{"document_root":MEDIA_ROOT}

    #富文本相关url
    # path('ueditor/',include('DjangoUeditor.urls' )),   #配置DjangoUeditor路径

    #富文本django-ckeditorurl配置
    path('ckeditor/',include('ckeditor_uploader.urls' )),   #配置django-ckeditorurl路径
]
