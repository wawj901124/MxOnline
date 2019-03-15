# _*_ coding:utf-8 _*_

__author__ = 'bobby'
__date__ = '2018/4/13 15:27'

from django.urls import path,include

from .views import OrgView
from .views import AddUserAskView   #导入AddUserAskView
from  .views import OrgHomeView   #导入OrgHomeView
from  .views import OrgCourseView  #导入OrgCourseView
from  .views import OrgDescView  #导入OrgDescView
from  .views import OrgTeacherView  #导入OrgTeacherView
from  .views import AddFavView  #导入AddFavView

urlpatterns = [
    #课程机构列表页
    path('list/', OrgView.as_view(), name="org_list"),  # 配置课程列表页面的访问路径
    path('add_ask/', AddUserAskView.as_view(), name="add_ask"),  # 配置课程列表页面的访问路径
    path('home/<path:org_id>/', OrgHomeView.as_view(), name="org_home"),
    path('course/<path:org_id>/', OrgCourseView.as_view(), name="org_course"),
    path('desc/<path:org_id>/', OrgDescView.as_view(), name="org_desc"),
    path('teacher/<path:org_id>/', OrgTeacherView.as_view(), name="org_teacher"),

    #机构收藏
    path('add_fav/', AddFavView.as_view(), name="add_fav"),
]

app_name = 'organiza'