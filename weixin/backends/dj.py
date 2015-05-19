#coding=utf8
'''
Created on 2014-5-14
django 帮助函数

@author: skycrab

@sns_userinfo
def oauth(request):
    openid = request.openid

'''
import json
from functools import wraps
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import redirect

from .common import CommonHelper
from .. import class_property, WeixinHelper


class Helper(CommonHelper):
    """微信具体逻辑帮组类"""

    @class_property
    def cache(cls):
        """返回cache对象"""
        return cache

    @class_property
    def secret_key(cls):
        """返回cookie加密秘钥"""
        return settings.SECRET_KEY



def sns_userinfo_callback(callback=None):
    """网页授权获取用户信息装饰器
    callback(openid, userinfo):
        return user
    """
    def wrap(func):
        @wraps(func)
        def inner(*args, **kwargs):
            request = args[0]  #django第一个参数request
            openid = request.COOKIES.get('openid')
            userinfo = None
            if not openid:
                code = request.GET.get("code")
                if not code:
                    current = "http://"+ request.get_host() + request.get_full_path()
                    return redirect(WeixinHelper.oauth2(current))
                else:
                    data = json.loads(WeixinHelper.getAccessTokenByCode(code))
                    access_token, openid, refresh_token = data["access_token"], data["openid"], data["refresh_token"]
                    #WeixinHelper.refreshAccessToken(refresh_token)
                    userinfo = json.loads(WeixinHelper.getSnsapiUserInfo(access_token, openid))
            else:
                ok, openid = Helper.check_cookie(openid)
                if not ok:
                    return redirect("/")
            request.openid = openid
            if callable(callback):
                request.user = callback(openid, userinfo)
            response = func(request)
            return response
        return inner
    return wrap

sns_userinfo = sns_userinfo_callback()

















