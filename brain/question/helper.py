#coding=utf8
'''
Created on 2014-5-14

@author: skycrab
'''
import hmac
import json
import traceback
from functools import wraps
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import redirect


from .weixin import WeixinHelper, class_property

def catch(func):
    @wraps(func)
    def wrap(*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except Exception as e:
            print(traceback.format_exc())
            return None
    return wrap


class Helper(object):
    """微信具体逻辑帮组类"""

    @class_property
    def access_token(cls):
        key = "ACCESS_TOKEN"
        token = cache.get(key)
        if not token:
            data = json.loads(WeixinHelper.getAccessToken())
            token, expire = data["access_token"], data["expires_in"]
            cache.set(key, token, expire-300)
        return token

    @class_property
    def jsapi_ticket(cls):
        key = "JSAPI_TICKET"
        ticket = cache.get(key)
        if not ticket:
            data = json.loads(WeixinHelper.getJsapiTicket(cls.access_token))
            ticket, expire = data["ticket"], data["expires_in"]
            cache.set(key, ticket, expire-300)
        return ticket

    @classmethod
    def hmac_sign(cls, key):
        return hmac.new(settings.SECRET_KEY, key).hexdigest()

    @classmethod
    def sign_cookie(cls, key):
        """cookie签名"""
        return "{0}|{1}".format(key, cls.hmac_sign(key))

    @classmethod
    def check_cookie(cls, value):
        """验证cookie
        成功返回True, key
        """
        code = value.split("|", 1)
        if len(code) != 2:
            return False, None
        key, signature = code
        if cls.hmac_sign(key) != signature:
            return False, None
        return True, key

    @classmethod
    def send_text_message(cls, openid, message):
        """客服主动推送消息"""
        return WeixinHelper.sendTextMessage(openid, message, cls.access_token)

    @classmethod
    def jsapi_sign(cls, url):
        """jsapi_ticket 签名"""
        return WeixinHelper.jsapiSign(cls.jsapi_ticket, url)


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
















