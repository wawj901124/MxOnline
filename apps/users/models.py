# _*_ encoding:utf-8 _*_
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser #导入引用django默认新建user表的类AbstractUser

# Create your models here.


class UserProfile(AbstractUser):   #新建自定义user表模型类，继承AbstractUser类
    nick_name = models.CharField(max_length=50, verbose_name=u"昵称", default="")   #新增加昵称字段
    birthday = models.DateField(verbose_name=u"生日",null=True, blank=True)   #新增加生日字段，可以为空不填写
    gender = models.CharField(max_length=6, choices=(("male",u"男"),("female",u"女")), default="female")   #新增加性别字段，只有两个值：男或女
    address = models.CharField(max_length=100, default=u"")   #新加地址字段
    mobile = models.CharField(max_length=11, null=True, blank=True)   #新加手机字段
    image = models.ImageField(upload_to="image/%Y/%m", default=u"image/default.png", max_length=100)   #新加头像字段

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):  #重载__unicode__使用__str__  #如果不重载此方法，在实例化的时候不能打印自定义的字符串
        return self.username


class EmailVerifyRecord(models.Model):   #新建邮箱验证码的models
    code = models.CharField(max_length=20, verbose_name=u"验证码")
    email = models.EmailField(max_length=50, verbose_name=u"邮箱")
    send_type = models.CharField(max_length=10, choices=(("register",u"注册"),("forget",u"找回密码")),verbose_name=u"验证码类型")
    send_time = models.DateTimeField(default=datetime.now, verbose_name=u"验证码发送时间")   #定义时间，用于验证码的过期验证datetime.now-获取实例化时间，datetime.now()-获取models编译的时间

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):  #重载__unicode__使用__str__  #重载unicode方法,貌似未生效
        return '{0}({1})'.format(self.code, self.email)



class Banner(models.Model):     #新建轮播图的models
    title = models.CharField(max_length=100, verbose_name=u"标题")
    image = models.ImageField( max_length=100, upload_to="banner/%Y/%m", verbose_name=u"轮播图")
    url = models.URLField(max_length=200, verbose_name=u"访问地址")
    index = models.IntegerField(default=100, verbose_name=u"顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name