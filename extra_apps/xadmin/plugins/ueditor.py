# _*_ coding:utf-8 _*_

__author__ = 'bobby'
__date__ = '2018/4/23 10:36'
import xadmin   #导入xadmin
from xadmin.views import BaseAdminPlugin,CreateAdminView,ModelFormAdminView,UpdateAdminView   #导入view
from DjangoUeditor.models import UEditorField   #导入UEditorField
from DjangoUeditor.widgets import UEditorWidget   #导入UEditorWidget
from django.conf import settings   #导入settings


class XadminUEditorWidget(UEditorWidget):   #继承UEditorWidget
    def __init__(self, **kwargs):
        self.ueditor_options = kwargs
        self.Media.js = None
        super(XadminUEditorWidget,self).__init__(kwargs)


class UeditorPlugin(BaseAdminPlugin):   #继承BaseAdminPlugin
    def get_field_style(self, attrs, db_field, style, **kwargs):
        if style =='ueditor':   #如果style是ueditor
            if isinstance(db_field, UEditorField):
                widget = db_field.formfield().widget
                param = {}
                param.update(widget.ueditor_settings)
                param.update(widget.attrs)
                return {'widget':XadminUEditorWidget(**param)}
        return attrs

    def block_extrahead(self, context, nodes):   #可以在生成的页面当中加入自己的js文件
        js = '<script type="text/javascript" src="%s"></script>'\
             % (settings.STATIC_URL+"ueditor/ueditor.config.js")   #自己的静态目录，引入的是ueditor/ueditor.config.js中的js文件
        js = '<script type="text/javascript" src="%s"></script>' \
             % (settings.STATIC_URL+"ueditor/ueditor.all.min.js")   #自己的静态目录，引入的是ueditor/ueditor.all.min.js中的js文件
        nodes.append(js)


xadmin.site.register_plugin(UeditorPlugin, UpdateAdminView)   #把UeditorPlugin这个plugin注册到UpdateAdminView中，UpdateAdminView代表修改页面
xadmin.site.register_plugin(UeditorPlugin, CreateAdminView)   #把UeditorPlugin这个plugin注册到CreateAdminView中，CreateAdminView代表新增页面

