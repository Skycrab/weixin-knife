#coding=utf8
'''
Created on 2014-5-14

@author: skycrab
'''
import hmac
import json
from functools import wraps
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import redirect


from .weixin import WeixinHelper, class_property


class Helper(object):
    """微信具体逻辑帮组类"""

    @class_property
    def access_token(cls):
        key = "ACCESS_TOKEN"
        token = cache.get(key)
        if not token:
            data = WeixinHelper.getAccessToken()
            token, expire = data["access_token"], data["expires_in"]
            cache.set(key, token, expire-300)
        return token

    @classmethod
    def sign_cookie(cls, key):
        """cookie签名"""
        return "{0}|{1}".format(key, hmac.new(settings.SECRET_KEY, key).hexdigest())

    @classmethod
    def check_cookie(cls, value):
        """验证cookie
        成功返回True, key
        """
        code = value.split("|", 1)
        if len(code) != 2:
            return False, None
        key, signature = code
        if cls.sign_cookie(key) != signature:
            return False, None
        return True, key


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
                    print userinfo
            request.openid = openid
            if callable(callback):
                request.user = callback(openid, userinfo)
            response = func(request)
            return response
        return inner
    return wrap

sns_userinfo = sns_userinfo_callback()
















