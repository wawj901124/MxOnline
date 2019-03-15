# _*_ encoding:utf-8 _*_
from datetime import datetime

from django.db import models
# from DjangoUeditor.models import UEditorField   #导入UEditorField,富文本编辑框
from ckeditor_uploader.fields import RichTextUploadingField #导入RichTextUploadingField,富文本编辑框

from organization.models import CourseOrg   #导入课程机构models

# Create your models here.


class Course(models.Model):   #课程类
    course_org = models.ForeignKey(CourseOrg, verbose_name=u"课程机构", null=True, blank=True, on_delete=models.CASCADE)   #新加字段，需要设置为可以为空，不然会问已有数据的内容的这个字段要填写什么
    name = models.CharField(max_length=50, verbose_name=u"课程名称")
    desc = models.CharField(max_length=300, verbose_name=u"课程描述")
    # detail = models.TextField(verbose_name=u"课程详情")
    detail = RichTextUploadingField(null=True, blank=True, verbose_name=u"课程详情")
    # detail = UEditorField(verbose_name=u"课程详情",width=600, height=300, imagePath="courses/ueditor/",
    #                       filePath="courses/ueditor/",default="")
    is_banner = models.BooleanField(default=False, verbose_name=u"是否轮播")

    degree = models.CharField(max_length=2, choices=(("cj","初级"),("zj","中级"),("gj","高级")), verbose_name=u"课程难度")
    learn_time = models.IntegerField(default=0, verbose_name=u"学习时长（分钟数）")
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    image = models.ImageField(max_length=100, upload_to="courses/%Y/%m", verbose_name=u"封面图")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        # 获取课程章节数
        return self.lesson_set.all().count()

    get_zj_nums.short_description = u"章节数"   #定义xadmin中显示get_zj_nums函数返回值的键的名字

    def go_to(self):   #定义点击课程后跳转到某一个地方（可以加html代码）
        from django.utils.safestring import mark_safe   #调用mark_safe这个函数，django可以显示成一个文本，而不是html代码
        return mark_safe("<a href='http://www.projectsedu.com'>跳转</a>")
        # return  "<a href='http://www.projectsedu.com'>跳转</a>"

    go_to.short_description = u"跳转"   #为go_to函数名个名字


    def get_learn_users(self):
        #获取用户学习课程统计，取得前五个
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        # 获取课程所有章节
        return self.lesson_set.all()


    def __str__(self):   #重载__unicode__使用__str__
        return self.name


class BannerCourse(Course):   #重新定义一个model，继承Course，为了在xadmin中注册而用
    class Meta:
        verbose_name = u"轮播课程"
        verbose_name_plural = verbose_name
        proxy = True  #将proxy设置为True,不会再生成一张表，如果不设置为True,就会再生成一张表
                        #将proxy设置为True,不会再生成一张表，同时具有model的属性


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程",on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=u"章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name

    def __str__(self):  #重载__unicode__使用__str__  #重载unicode方法,貌似未生效
        return '{0}({1})'.format(self.course, self.name)


class Video(models.Model):   #视频类
    lesson = models.ForeignKey(Lesson, verbose_name=u"章节", on_delete=models.CASCADE)   #外键，用于进行多对一，多对多的映射
    name = models.CharField(max_length=100, verbose_name=u"视频名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name


class CourseResource(models.Model):   #资源下载类
    course = models.ForeignKey(Course, verbose_name=u"课程", on_delete=models.CASCADE)   #外键，用于进行多对一，多对多的映射
    name = models.CharField(max_length=100, verbose_name=u"名称")
    download = models.FileField(max_length=100,upload_to="course/resource/%Y%m", verbose_name=u"资源文集")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name

