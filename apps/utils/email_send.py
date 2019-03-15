# _*_ coding:utf-8 _*_

__author__ = 'bobby'
__date__ = '2018/4/9 16:34'
from random import Random   #导入Random
from django.core.mail import send_mail   #导入django内部的发送邮件函数send_mail

from users.models import EmailVerifyRecord   #导入邮箱验证码model
from MxOnline.settings import EMAIL_FROM   #导入发件人EMAIL_FROM


def send_register_email(email, send_type="register"):
    email_record = EmailVerifyRecord()   #实例化
    code = generate_random_str(16)   #生成一个16位长的字符
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()   #保存一下，把要发送的code事先保存到数据库当中

    email_title = ""   #定义邮箱标题为空串
    email_body = ""   #定义邮箱正文为空串

    if send_type == "register":   #如果为注册码
        email_title = u"慕学在线网注册激活链接"
        email_body = u"请点击下面的链接激活你的账号：http://127.0.0.1:8001/active/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])   #调用邮件发送函数,会返回一个值
        if send_status:   #如果发送成功
            pass

    elif send_type == "forget":   #如果为找回密码类型
        email_title = u"慕学在线网密码重置链接"
        email_body = u"请点击下面的链接重置密码：http://127.0.0.1:8001/reset/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])   #调用邮件发送函数,会返回一个值
        if send_status:   #如果发送成功
            pass


def generate_random_str(randomlength=8):
    str =  ''  #定义一个空字符串
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqIiSsTtUuVvWwXxYyZz0123456789'
    lentgh = len(chars) -1
    random = Random()   #调用Random(),根据长度随机生成数字
    for i in range(randomlength):
        str += chars[random.randint(0,lentgh)]
    return str


