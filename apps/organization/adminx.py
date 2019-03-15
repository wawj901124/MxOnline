# _*_ coding:utf-8 _*_

__author__ = 'bobby'
__date__ = '2018/4/3 18:15'

import xadmin

from .models import CityDict
from .models import CourseOrg
from .models import Teacher


class CityDictAdmin(object):
    diduan = ['name', 'desc', 'add_time']
    list_display = diduan   #定义显示的字段
    search_fields = diduan   #定义搜索的字段
    list_filter = diduan   #定义筛选的字段

xadmin.site.register(CityDict, CityDictAdmin)


class CourseOrgAdmin(object):
    diduan = ['name', 'desc','click_nums', 'fav_nums', 'image', 'address', 'city', 'add_time']
    list_display = diduan   #定义显示的字段
    search_fields = diduan   #定义搜索的字段
    list_filter = diduan   #定义筛选的字段
    relfield_style = 'fx-ajax'   #当有的模块以该模块为外键时，可以进行ajax动态搜索

xadmin.site.register(CourseOrg, CourseOrgAdmin)


class TeacherAdmin(object):
    diduan = ['org', 'name', 'work_years','work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'add_time']
    list_display = diduan   #定义显示的字段
    search_fields = diduan   #定义搜索的字段
    list_filter = diduan   #定义筛选的字段

xadmin.site.register(Teacher, TeacherAdmin)

