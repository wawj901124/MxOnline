"""
Django settings for MxOnline project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,os.path.join(BASE_DIR,'apps'))
sys.path.insert(0,os.path.join(BASE_DIR,'extra_apps'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1i8r_eop66y1i9tm+)odg9%v3vjzuh+n+%8)&th#2d=aty*)@1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
AUTHENTICATION_BACKENDS = (
    'users.views.CustomBackend',

)   #重载此变量后，可以使用邮箱登陆

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',  #注册app
    'courses',   #注册app
    'organization',   #注册app
    'operation',   #注册app
    'xadmin',    #注册xadmin
    'crispy_forms',   #注册xadmin的依赖应用crispy_forms
    'captcha',   #注册生成图片验证码的应用
    'pure_pagination',   #注册分页库
    # 'DjangoUeditor',   #注册 DjangoUeditor
    'ckeditor',#注册富文本包ckeditor
    'ckeditor_uploader'#注册富文本附带包ckeditor_uploader
]

AUTH_USER_MODEL = "users.UserProfile"   #重载AUTH_USER_MODEL方法


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MxOnline.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',   #导入media上下文的处理器，为了使配置的{{MEDIA_URL}}生效
            ],
        },
    },
]

WSGI_APPLICATION = 'MxOnline.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "mxonline",
        'USER':"root",
        'PASSWORD':"",
        'HOST':"127.0.0.1"
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

# LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'

LANGUAGE_CODE = 'zh-hans'   #语言改为中文

TIME_ZONE = 'Asia/Shanghai'   #时区设置为上海

USE_I18N = True

USE_L10N = True

# USE_TZ = True
USE_TZ = False   #时间为本地时间，即上海时间，如果为True，则时间取得的是UTC的时间，即国际时间


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'   #配置静态路径根目录
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)   #STATICFILES_DIRS指明static文件目录


#配置发送邮件的信息
EMAIL_HOST = "mail.iapppay.com"   #配置发送邮箱的服务器smtp
EMAIL_PORT = 25   #一般固定为25
EMAIL_HOST_USER = "xiangkaizheng@iapppay.com"    #配置可用邮箱登录账号
EMAIL_HOST_PASSWORD = "iapppay002"   #配置可用邮箱登录密码
# EMAIL_HOST_PASSWORD = "admin123"   #配置邮箱登录密码
EMAIl_USE_TLS = False   #默认配置此参数为False即可
EMAIL_FROM = "xiangkaizheng@iapppay.com"   #指明发件人，要与EMAIL_HOST_USER 一致，不一致会出错


MEDIA_URL = '/media/'   #配置上传文件跟目录
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')    #MEDIA_ROOT只能设置一个，根目录,把media与根目录BASE_DIR连接起来
CKEDITOR_UPLOAD_PATH = 'images/'   #富文本django-ckeditor上传文件路径
