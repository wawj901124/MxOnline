# _*_ coding:utf-8 _*_

__author__ = 'bobby'
__date__ = '2018/4/9 11:32'
from django import forms    #导入django中的forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):   #继承Form
    username = forms.CharField(required=True)   #required=True表示字段不能为空，为空就会报错,是必填字段
    password = forms.CharField(required=True,min_length=5)   #此处的字段定义必须与html页面中的form中字段的名字是一样的


class RegisterForm(forms.Form):   #对注册页面的表单进行验证
    email = forms.EmailField(required=True)   #对email的验证
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={"invalid":u"自定义验证码错误"})   #对图像验证码进行验证,自定义错误提示


class ForgetForm(forms.Form):   #对注册页面的表单进行验证
    email = forms.EmailField(required=True)   #对email的验证
    captcha = CaptchaField(error_messages={"invalid":u"自定义验证码错误"})   #对图像验证码进行验证,自定义错误提示


class ModifyPwdForm(forms.Form):   #对修改密码的页面的表单进行验证
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)
