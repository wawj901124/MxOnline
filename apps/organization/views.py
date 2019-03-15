from django.shortcuts import render
from django.views.generic import View   #导入View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger #分页导入包
from django.http import HttpResponse   #导入HttpResponse ，用于指定返回的类型，返回的是json字符串

from .models import CourseOrg #导入课程机构模型
from .models import CityDict   #导入城市模型
from operation.models import UserFavorite   #导入收藏模块
from .forms import UserAskForm   #导入UserAskForm
from .forms import UserAskForm   #导入UserAskForm


from courses.models import Course   #导入Course


# Create your views here.
class OrgView(View):   #编写处理前段页面课程首页（列表）的View
    """课程机构列表功能"""
    def get(self, request):
        #课程机构
        all_orgs = CourseOrg.objects.all()   #获取所有课程机构的数据
        hot_orgs = all_orgs.order_by("-click_nums")[:3]   #根据点击量click_nums进行排序，然后选前3个作为热门机构
        #城市
        all_citys =CityDict.objects.all()   #获取所有的城市

        #取出筛选城市
        city_id  =  request.GET.get("city","")
        if city_id: #如果有这个值
            all_orgs  = all_orgs.filter(city_id = int(city_id))   #取出对应城市的数据

        #类别筛选
        category = request.GET.get("ct","")
        if category:   #如果有类别的话
            all_orgs = all_orgs.filter(category = category)   #做类别的筛选

        #排序筛选
        sort = request.GET.get("sort", "")
        if sort:#如果有值
            if sort == "students":#如果为学习人数
                all_orgs = all_orgs.order_by("-students")   #根据学习人数排序
            elif sort == "courses":#如果为课程人数
                all_orgs = all_orgs.order_by("-course_nums")    #根据课程数排序



        org_nums = all_orgs.count()  # 获取课程机构的数量

        #对课程机构进行分页
        try:
            page = request.GET.get('page', 1)     #取第一页
        except PageNotAnInteger:
            page = 1                        #取第一页
        p = Paginator(all_orgs, 5, request=request)   #自动对all_orgs（获取的所有课程机构的数据）进行分页，每页5个
        orgs = p.page(page)   #取与页数相对的数据


        return render(request, 'org-list.html', {
            "all_orgs":orgs,
            "all_citys":all_citys,
            "org_nums":org_nums,
            "city_id":city_id,
            "category":category,   #传入类别到html页面
            "hot_orgs":hot_orgs,   #传入热门机构
            "sort":sort
        })


class AddUserAskView(View):   #处理‘我要学习’表单的view
    """
    用户添加咨询   #添加注释
    """
    def post(self, request):   #此处表单只有一个post请求，表单的请求
        userask_form = UserAskForm(request.POST)   #实例化
        if userask_form.is_valid():   #如果合法
            user_ask = userask_form.save(commit=True)   #commit=True表示提交后直接保存到数据库commit=False表示只是表单提交数据，没有保存到数据库
            return  HttpResponse('{"status":"success"}', content_type='application/json')   #返回json串，正确，返回成功,content_type用来指明字符串的格式,此处指明为json
        else:
            # return HttpResponse("{'status':'fail', 'msg':'添加出错'}", content_type='application/json')
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json') #失败，返回失败原因,content_type='application/json'为固定的写法


class OrgHomeView(View):   #建立对机构首页处理的view
    """
    机构首页
    """
    def get(self,request, org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False   #用户是否收藏
        if request.user.is_authenticated: #如果用户登录
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type = 2):#如果查到收藏
                has_fav = True

        all_courses = course_org.course_set.all()[:3]#course_set,反向取所有的course  #取出所有课程,只取3个
        all_teachers = course_org.teacher_set.all()[:1] #取出所有的教师，再从所有的教师中取出1个
        return render(request,"org-detail-homepage.html",{
            "all_courses":all_courses,
            "all_teachers":all_teachers,
            "course_org":course_org,
            "current_page":current_page,
            "has_fav": has_fav,
        })


class OrgCourseView(View):   #建立对机构课程列表页处理的view
    """
    机构课程列表页
    """
    def get(self,request, org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))   #取出机构
        has_fav = False  # 用户是否收藏
        if request.user.is_authenticated:  # 如果用户登录
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):  # 如果查到收藏
                has_fav = True

        all_courses = course_org.course_set.all()#course_set,反向取所有的course  #取出所有课程
        return render(request,"org-detail-course.html",{
            "all_courses":all_courses,
            "course_org":course_org,
            "current_page": current_page,
            "has_fav": has_fav,
        })


class OrgDescView(View):   #建立对机构介绍页处理的view
    """
    机构介绍页
    """
    def get(self,request, org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))   #取出机构
        has_fav = False  # 用户是否收藏
        if request.user.is_authenticated:  # 如果用户登录
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):  # 如果查到收藏
                has_fav = True

        return render(request,"org-detail-desc.html",{
            "course_org":course_org,
            "current_page": current_page,
            "has_fav": has_fav,
        })


class OrgTeacherView(View):   #建立对机构讲师页处理的view
    """
    机构教师页
    """
    def get(self,request, org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))   #取出机构
        has_fav = False  # 用户是否收藏
        if request.user.is_authenticated:  # 如果用户登录
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):  # 如果查到收藏
                has_fav = True

        all_teachers = course_org.teacher_set.all()#course_set,反向取所有的course  #取出所有教师
        return render(request,"org-detail-teachers.html",{
            "all_teachers":all_teachers,
            "course_org":course_org,
            "current_page": current_page,
            "has_fav": has_fav,
        })


class AddFavView(View):  #建立处理收藏的View
    """
    用户收藏以及用户取消收藏
    """
    def post(self,request):
        fav_id = request.POST.get('fav_id', 0)    #获取收藏id,默认设置为0
        fav_type = request.POST.get('fav_type', 0)   #获取收藏类型，默认设置为0

        if request.user.is_authenticated:   #判断用户是否登录，如果未登录,is_authenticated为True,表示用户未登录
            #判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}',
                                content_type='application/json')  # 失败，返回失败原因,content_type='application/json'为固定的写法 #后台控制不了ajax跳转，跳转在ajax中进行
        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type = int(fav_type))
        if exist_records:
                # 如果记录已经存在，则表示用户取消收藏
                exist_records.delete()   #存在则删掉
                return HttpResponse('{"status":"fail", "msg":"收藏"}',
                                    content_type='application/json')

        else:#如果不存在，则在数据库里添加记录
                user_fav = UserFavorite()   #实例化
                if int(fav_id) >0 and int(fav_type)>0:   #如果都大于0，则添加
                    user_fav.user = request.user
                    user_fav.fav_id = int(fav_id)
                    user_fav.fav_type = int(fav_type)
                    user_fav.save()   #保存，添加到数据库
                    return HttpResponse('{"status":"success", "msg":"已收藏"}',
                                        content_type='application/json')  # 失败，返回失败原因,content_type='application/json'为固定的写法 #后台控制不了ajax跳转，跳转在ajax中进行
                else:
                    return HttpResponse('{"status":"fail", "msg":"收藏出错"}',
                                        content_type='application/json')  # 失败，返回失败原因,content_type='application/json'为固定的写法 #后台控制不了ajax跳转，跳转在ajax中进行









