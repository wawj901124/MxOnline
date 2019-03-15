# _*_ coding:utf-8 _*_

__author__ = 'bobby'
__date__ = '2018/4/23 11:58'
import  xadmin   #导入xadmin
from xadmin.views import BaseAdminPlugin,ListAdminView
from django.template import loader


#excel导入
class ListImportExcelPlugin(BaseAdminPlugin):   #继承BaseAdminPlugin
    import_excel = False  #设置默认一个变量，为False

    def init_request(self, *args, **kwargs): #init_request返回为True时，才会加载此插件#确定是否加载插件
        return bool(self.import_excel)

    def block_top_toolbar(self, context, nodes):   #将自己的html文件显示到某一个地方
        nodes.append(
            loader.render_to_string(
                'xadmin/excel/model_list.top_toolbar.import.html',
                {"context":context}
            )   #重载 loader.render_to_string函数，就会把自定义的html页面方到xadmin中
        )

xadmin.site.register_plugin(ListImportExcelPlugin,ListAdminView)   #注册到xadmin中的ListAdminView中
