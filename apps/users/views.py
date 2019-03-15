from django.shortcuts import render
from django.contrib.auth import authenticate #导入authenticate方法来验证用户名和密码
from django.contrib.auth import login #导入login方法进行用户登录
from django.contrib.auth.backends import ModelBackend   #用于认证backends
from django.db.models import  Q   #Q可以完成并集“或”的逻辑
from django.views.generic.base import View   #导入view
from django.contrib.auth.hashers import make_password #导入make_password,对密码的明文进行加密

from .models import UserProfile
from .models import EmailVerifyRecord   #导入models中的EmailVerifyRecord
from .forms import LoginForm   #导入forms中的LoginForm
from .forms import RegisterForm #导入forms中的RegisterForm
from .forms import ForgetForm   #导入forms中的ForgetForm
from .forms import ModifyPwdForm   #导入forms中的ModifyPwdForm
from utils.email_send import send_register_email   #导入发送注册邮件方法



class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):   #自动调用authenticate方法
        #设置自己的后台逻辑
        try:
            user = UserProfile.objects.get(Q(username = username)|Q(email = username))   #用Q完成并集的查询
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class ActiveUserView(View): #处理active的active_code所用
    def get(self, request, active_code):   #把提取到的active_code返回回来
        all_records = EmailVerifyRecord.objects.filter(code = active_code)   #在数据库中EmailVerifyRecord模型生成的表中查找到与code字段与active_code匹配的所有记录
        if all_records:   #如果all_records不为空
            for record in all_records:   #遍历查询每一条记录
                email = record.email
                user = UserProfile.objects.get(email=email)   #在UserProfile模型生成的表中查找到相应email的用户记录
                user.is_active = True   #将UserProfile模型生成的表中查找到相应email的用户的is_active字段改为激活状态True
                user.save()   #保存
        else:
            return render(request, "active_fail.html")  # 为匹配到记录，提示链接无效
        return render(request, "login.html")   #激活之后跳转到登录页面




class RegisterView(View):   #处理前段注册页面的view类
    def get(self, request):
        register_form = RegisterForm()   #实例化RegisterForm()
        return render(request, "register.html", {'register_form':register_form})  # 把用户的页面返回给浏览器

    def post(self, request):
        register_form = RegisterForm(request.POST)  # 实例化RegisterForm()
        if register_form.is_valid():  # is_valid()判断是否有错
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):   #查询该邮箱是否已经被注册，如果已经注册
                return render(request, "register.html", {"register_form": register_form, 'msg': "用户已经存在"})  # 把用户的页面返回给浏览器,回填用户信息
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()   #实例化 UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False   #is_active字段为False表示用户还未激活
            user_profile.password = make_password(pass_word)   #对明文进行加密
            user_profile.save()   #将注册信息保存到数据库中

            send_register_email(user_name,"register")   #调用发送注册邮件的方法
            return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form": register_form})   #回填用户信息






class LoginView(View):   #基于view 类的使用,处理前段请求的view类
    def get(self, request):
        return render(request, "login.html", {})  # 把用户的页面返回给浏览器

    def post(self,request):
        login_form = LoginForm(request.POST)   #实例化LoginForm
        if login_form.is_valid():   #is_valid()判断是否有错
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name,password=pass_word)   #如果authenticate验证通过会返回一个对象，如果不通过就是个None
                                                    #authenticate方法是向数据库发起验证，看用户名和密码是否正确
                                                    #authenticate传参数时一定要写上参数名称username = user_name,password = pass_word，否则报错
            if user is not None:
                if user.is_active:   #user为激活状态才能登录
                    login(request, user)   #调用login()方法进行登录，第一个参数为request,第二个参数是用户登录信息
                    return render(request, "index.html")   #登录成功后返回一个页面，跳转到一个页面
                else:
                    return render(request, "login.html", {"msg": "用户未激活！"})   #登录失败，提示用户未激活
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误！"})
        else:
            return render(request, "login.html", {"login_form":login_form})








# Create your views here.
def user_login(request):
    if request.method == "POST":   #用户登录的时候一般都用post,这样相对安全些
        user_name = request.POST.get("username", "")
        pass_word = request.POST.get("password", "")
        user = authenticate(username=user_name,password=pass_word)   #如果authenticate验证通过会返回一个对象，如果不通过就是个None
                                                #authenticate方法是向数据库发起验证，看用户名和密码是否正确
                                                #authenticate传参数时一定要写上参数名称username = user_name,password = pass_word，否则报错

        if user is not None:
            login(request, user)   #调用login()方法进行登录，第一个参数为request,第二个参数是用户登录信息
            return render(request, "index.html")   #登录成功后返回一个页面，跳转到一个页面
        else:
            return render(request, "login.html", {"msg":"用户名或密码错误！"})

    elif request.method == "GET":
        return render(request, "login.html", {})   #把用户的页面返回给浏览器


class ForgetPwdView(View):   #处理前段找回密码页面的view类
    def get(self, request):
        forget_form = ForgetForm()   #实例化
        return render(request, "forgetpwd.html", {'forget_form':forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)   #实例化，初始化
        if forget_form.is_valid():   #如果表单提交不为空，如果合法的情况下
            email = request.POST.get("email", "")   #取出email内容
            send_register_email(email, "forget")
            return render(request, "send_success.html")
        else:
            return render(request, "forgetpwd.html",{"forget_form":forget_form})


class ResetView(View): #处理Reset的active_code所用
    def get(self, request, active_code):   #把提取到的active_code返回回来
        all_records = EmailVerifyRecord.objects.filter(code = active_code)   #在数据库中EmailVerifyRecord模型生成的表中查找到与code字段与active_code匹配的所有记录
        if all_records:   #如果all_records不为空
            for record in all_records:   #遍历查询每一条记录
                email = record.email   #获取email
                return render(request, "password_reset.html",{"email":email})  # 如果匹配成功，则返回给用户重置密码页面
        else:
            return render(request, "active_fail.html")  # 未匹配到记录，提示链接无效
        return render(request, "login.html")   #激活之后跳转到登录页面


class ModifyPwdView(View):   #处理修改密码页面的View类
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():   #如果合法
            pwd1 = request.POST.get("password1", "")   #取到password1中的内容
            pwd2 = request.POST.get("password2", "")  # 取到password2中的内容
            email = request.POST.get("email", "")
            if pwd1 != pwd2:   #如果两次输入的密码不相同
                return render(request, "password_reset.html", {"email": email, "msg":"密码不一致" })  # 返回页面，提示两次密码不相同
            user = UserProfile.objects.get(email=email)   #通过email查到相应用户
            user.password = make_password(pwd2)   #将查到的用户密码改为修改后的密码

            user.save()   #将修改后的密码保存到数据库中

            return render(request, "login.html")  # 修改密码完成之后跳转到登录页面
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})  # 返回页面，提示两次密码不相同



