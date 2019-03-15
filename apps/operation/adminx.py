# _*_ coding:utf-8 _*_

__author__ = 'bobby'
__date__ = '2018/4/3 18:15'

import xadmin

from .models import UserAsk
from .models import CourseComments
from .models import UserFavorite
from .models import UserMessage
from .models import UserCourse

class UserAskAdmin(object):
    diduan = ['name', 'mobile', 'course_name', 'add_time']
    list_display = diduan  # 定义显示的字段
    search_fields = diduan  # 定义搜索的字段
    list_filter = diduan  # 定义筛选的字段

xadmin.site.register(UserAsk, UserAskAdmin)


class CourseCommentsAdmin(object):
    diduan = ['user', 'course', 'comments', 'add_time']
    list_display = diduan  # 定义显示的字段
    search_fields = diduan  # 定义搜索的字段
    list_filter = diduan  # 定义筛选的字段

xadmin.site.register(CourseComments, CourseCommentsAdmin)


class UserFavoriteAdmin(object):
    diduan = ['user', 'fav_id', 'fav_type', 'add_time']
    list_display = diduan  # 定义显示的字段
    search_fields = diduan  # 定义搜索的字段
    list_filter = diduan  # 定义筛选的字段

xadmin.site.register(UserFavorite, UserFavoriteAdmin)


class UserMessageAdmin(object):
    diduan = ['user', 'message', 'has_read', 'add_time']
    list_display = diduan  # 定义显示的字段
    search_fields = diduan  # 定义搜索的字段
    list_filter = diduan  # 定义筛选的字段

xadmin.site.register(UserMessage, UserMessageAdmin)


class UserCourseAdmin(object):
    diduan = ['user', 'course', 'add_time']
    list_display = diduan  # 定义显示的字段
    search_fields = diduan  # 定义搜索的字段
    list_filter = diduan  # 定义筛选的字段

xadmin.site.register(UserCourse, UserCourseAdmin)

