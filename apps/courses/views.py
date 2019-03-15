from django.shortcuts import render
from django.views.generic import View   #导入

# Create your views here.
class OrgView(View):   #编写处理前段页面课程首页（列表）的View
    """课程机构列表功能"""
    def get(self, request):
        return render(request, 'course-list.html', {})
