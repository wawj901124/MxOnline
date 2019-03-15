# _*_ coding:utf-8 _*_

__author__ = 'bobby'
__date__ = '2018/4/13 15:08'
import re   #导入正则表达式的包re
from django import forms

from operation.models import  UserAsk   #导入model,UserAsk

# class UserAskForm(forms.Form):   #定义处理前段“我要学习”表单类,继承Form，Form不能save,就没有save属性
#     name = forms.CharField(required=True, min_length=2, min_length=20)
#     phone = forms.CharField(required=True, min_length=11, max_length=11)
#     course_name = forms.CharField(required=True,min_length=5, max_length=50)

class UserAskForm(forms.ModelForm): #定义处理前段“我要学习”表单类,继承ModelForm,ModelForm可以直接save,这个save调用的就是model的save，可以直接保存到数据库
    class Meta:
        model = UserAsk   #指明转换的model为UserAsk
        fields = ['name','mobile','course_name']   #指明要转换的字段

    def clean_mobile(self):   #定义对字段mobile验证, clean 方法实际上是对每个字段进行了进一层的自定义
        """
        验证手机号码是否合法
        """
        moblie = self.cleaned_data['mobile']   #取出form中的mobile
        REGEX_MOBILE = "^1[3578]\d{9}$|^147\d{8}$|176\d{8}$"   #表示手机号的正则表达式规则
        p = re.compile(REGEX_MOBILE)   #匹配正则表达式
        if p.match(moblie): #如果取得的mobile 取得的值与正则表达式匹配
            return moblie
        else:   #否则抛出异常,错误为手机号码非法，自定义了一个code
            raise forms.ValidationError(u"手机号码非法", code="mobile_invalid")





