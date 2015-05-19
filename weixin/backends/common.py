#coding=utf8
'''
Created on 2014-5-19
通用帮助函数

@author: skycrab
'''
import hmac
import json

from .. import WeixinHelper, class_property


class CommonHelper(object):

    @class_property
    def expire(cls):
        """比真实过期减少时间"""
        return 300

    @class_property
    def cache(cls):
        """返回cache对象"""


    @class_property
    def access_token_key(cls):
        return "ACCESS_TOKEN"

    @class_property
    def jsapi_ticket_key(cls):
        return "JSAPI_TICKET"


    @class_property
    def access_token(cls):
        cache, key = cls.cache, cls.access_token_key
        token = cache.get(key)
        if not token:
            data = json.loads(WeixinHelper.getAccessToken())
            token, expire = data["access_token"], data["expires_in"]
            cache.set(key, token, expire-cls.expire)
        return token


    @class_property
    def jsapi_ticket(cls):
        cache, key = cls.cache, cls.jsapi_ticket_key
        ticket = cache.get(key)
        if not ticket:
            data = json.loads(WeixinHelper.getJsapiTicket(cls.access_token))
            ticket, expire = data["ticket"], data["expires_in"]
            cache.set(key, ticket, expire-cls.expire)
        return ticket

    @classmethod
    def send_text_message(cls, openid, message):
        """客服主动推送消息"""
        return WeixinHelper.sendTextMessage(openid, message, cls.access_token)

    @classmethod
    def jsapi_sign(cls, url):
        """jsapi_ticket 签名"""
        return WeixinHelper.jsapiSign(cls.jsapi_ticket, url)


    @classmethod
    def hmac_sign(cls, key):
        return hmac.new(cls.secret_key, key).hexdigest()

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





