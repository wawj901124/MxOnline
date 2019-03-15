# _*_ coding:utf-8 _*_

__author__ = 'bobby'
__date__ = '2018/4/3 18:15'

import xadmin


from .models import Course
from .models import Lesson
from .models import Video
from .models import CourseResource
from .models import BannerCourse
from organization.models import CourseOrg



class LessonInline():  #为了可以在添加课程的时候直接添加章节
    model = Lesson
    extra = 0


class CourseResourceInline(object): #对课程资源model做inline
    model = CourseResource
    extra = 0


class CourseAdmin(object):
    diduan = ['name', 'desc', 'detail','is_banner', 'degree',
              'learn_time', 'students', 'fav_nums', 'image', 'click_nums', 'add_time',
              ]

    list_display = ['name', 'desc', 'detail','is_banner', 'degree',
              'learn_time', 'students', 'fav_nums', 'image', 'click_nums', 'add_time',
              'get_zj_nums','go_to']   #定义显示的字段
    search_fields = diduan   #定义搜索的字段
    list_filter = diduan   #定义筛选的字段
    model_icon = 'fa fa-address-book-o'  # 定义图标显示
    ordering = ['-add_time']   #添加默认排序规则显示排序，根据点击人数倒序排序
    readonly_fields = ['click_nums']   #设置某些字段为只为可读  #设置了readonly_fields，再设置exclude，exclude对该字段无效，
    exclude = ['fav_nums']   #设置某些字段为不显示，即隐藏  #readonly_fields和exclude设置会有冲突
    inlines = [LessonInline,CourseResourceInline ]   #inlines配和LessonInline使用，可以直接在课程页面添加章节#只能做一层嵌套，不能进行两层嵌套
    list_editable = ['degree', 'desc']    #可以在列表页对字段进行编辑
    refresh_times = [3,5]  #对列表页进行定时刷新,配置了3秒和5秒，可以从中选择一个
    # style_fields = {"detail":"ueditor"}   #指明"detail"这个字段采用ueditor的样式，style_fields指明某个字段采用什么样式
    import_excel = True   #配置导入插件的import_excel变量，会覆盖插件中配置的import_excel变量

    def queryset(self):   #重载queryset方法，用来做到不同的admin取出的数据不同
        qs = super(CourseAdmin, self).queryset()   #调用父类
        qs = qs.filter(is_banner = False)   #通过is_banner字段筛选出轮播图
        return qs   #返回qs

    def save_models(self):   #重载save_models的方法，可以在做了某个动作后，动态重新加载
        #在保存课程的时候统计课程机构的课程数
        obj = self.new_obj   #取得当前课程的实例
        obj.save()   #保存当前课程
        if obj.course_org is not None:   #如果当前课程存在
            course_org = obj.course_org   #获取当前的course_org字段
            course_org.course_nums = Course.objects.filter(course_org = course_org).count()   #取得课程数
            course_org.save()   #保存到数据库

    def post(self,request, *args, **kwargs):  #重载post函数，获取excel文件
        if 'excel' in request.FILES:
            pass
        return super(CourseAdmin, self).post(request,args,kwargs)  # 调用父类post方法



xadmin.site.register(Course, CourseAdmin)


class BannerCourseAdmin(object):
    diduan = ['name', 'desc', 'detail', 'is_banner','degree','learn_time', 'students', 'fav_nums', 'image', 'click_nums', 'add_time']
    list_display = diduan   #定义显示的字段
    search_fields = diduan   #定义搜索的字段
    list_filter = diduan   #定义筛选的字段
    model_icon = 'fa fa-address-book-o'  # 定义图标显示
    ordering = ['-add_time']   #添加默认排序规则显示排序，根据点击人数倒序排序
    readonly_fields = ['click_nums']   #设置某些字段为只为可读  #设置了readonly_fields，再设置exclude，exclude对该字段无效，
    exclude = ['fav_nums']   #设置某些字段为不显示，即隐藏  #readonly_fields和exclude设置会有冲突
    inlines = [LessonInline,CourseResourceInline ]   #inlines配和LessonInline使用，可以直接在课程页面添加章节#只能做一层嵌套，不能进行两层嵌套

    import_excel = True


    def queryset(self):   #重载queryset方法，用来做到不同的admin取出的数据不同
        qs = super(BannerCourseAdmin, self).queryset()   #调用父类
        qs = qs.filter(is_banner = True)   #通过is_banner字段筛选出轮播图
        return qs   #返回qs

    def post(self,request, *args, **kwargs):  #重载post函数，获取excel文件
        if 'excel' in request.FILES:
            pass
        return super(BannerCourseAdmin, self).post(request,args,kwargs)   #调用父类post方法


xadmin.site.register(BannerCourse, BannerCourseAdmin)

class LessonAdmin(object):
    diduan = ['course', 'name', 'add_time']
    list_display = diduan   #定义显示的字段
    search_fields = diduan   #定义搜索的字段
    list_filter = ['course__name', 'name', 'add_time']  #定义筛选的字段

xadmin.site.register(Lesson, LessonAdmin)


class VideoAdmin(object):
    diduan = ['lesson', 'name', 'add_time']
    list_display = diduan   #定义显示的字段
    search_fields = diduan   #定义搜索的字段
    list_filter = diduan   #定义筛选的字段

xadmin.site.register(Video, VideoAdmin)


class CourseResourceAdmin(object):
    diduan = ['course', 'name', 'download', 'add_time']
    list_display = diduan   #定义显示的字段
    search_fields = diduan   #定义搜索的字段
    list_filter = diduan   #定义筛选的字段
    
xadmin.site.register(CourseResource, CourseResourceAdmin)

