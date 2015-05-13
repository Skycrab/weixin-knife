#coding=utf8
'''
Created on 2014-5-13

@author: skycrab
'''
import time
from collections import defaultdict
from .lib import WeixinHelper, ObjectDict


class MessageHandle(object):
    """消息处理器"""
    handler = defaultdict(dict)
    def __init__(self, xml):
        self.xml = ObjectDict(WeixinHelper.xmlToArray(xml))


    def start(self):
        """开始消息处理"""
        msgtype = self.xml.MsgType
        if msgtype == "event":
            key = self.xml.Event
        elif msgtype == "text":
            key = "all"
        else:
            key = ""

        return self.call(msgtype, key)


    def call(self, type, key):
        """回调事件"""
        assert type in self.handler
        data = self.handler[type][key](self.xml)
        response = self.render(data)
        return response


    @classmethod
    def register(cls, type, key, func):
        """注册事件"""
        assert key not in cls.handler
        cls.handler[type][key] = func

    def render(self, data):
        """消息回复"""
        if not data:
            return ""
        reply = Reply(self.xml)
        if isinstance(data, str):
            res = reply.textResponse(data)
        elif isinstance(data, dict):
            res = reply.newsResponse([data])
        elif isinstance(data, list): #只有图片可多条消息
            data = [reply.newsKey(d) for d in data]
            res = reply.newsResponse(data)
        else:
            raise Exception("unknown message response")

        return res


_TEXT = """\
    <xml>
    <ToUserName><![CDATA[{FromUserName}]]></ToUserName>
    <FromUserName><![CDATA[{ToUserName}]]></FromUserName>
    <CreateTime>{CreateTime}</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[{Content}]]></Content>
    </xml>"""

_ITEM = """\
    <item>
    <Title><![CDATA[{Title}]]></Title>
    <Description><![CDATA[{Description}]]></Description>
    <PicUrl><![CDATA[{PicUrl}]]></PicUrl>
    <Url><![CDATA[{Url}]]></Url>
    </item>"""

_NEWS = """\
    <xml>
    <ToUserName><![CDATA[{FromUserName}]]></ToUserName>
    <FromUserName><![CDATA[{ToUserName}]]></FromUserName>
    <CreateTime>{CreateTime}</CreateTime>
    <MsgType><![CDATA[news]]></MsgType>
    <ArticleCount>{ArticleCount}</ArticleCount>
    <Articles>
    {Items}
    </Articles>
    </xml>"""

class Reply(object):
    """消息回复"""
    def __init__(self, xml):
        self.xml = xml
        self.xml["CreateTime"] = int(time.time())

    def textResponse(self, data):
        """文本消息回复"""
        self.xml["Content"] = data
        return _TEXT.format(**self.xml)


    def newsKey(self, ld):
        """图文消息列表转换为字典"""
        return dict(zip(["Title", "Description", "PicUrl", "Url"], ld))

    def newsResponse(self, data):
        """图文消息"""
        count = len(data)
        if count > 10:
            raise Exception("ArticleCount greater then 10")
        self.xml["Items"] = "".join([_ITEM.format(**d) for d in data])
        self.xml["ArticleCount"] = count
        return _NEWS.format(**self.xml)



R = MessageHandle.register

def subscribe(func):
    """关注事件"""
    R("event", "subscribe", func)
    return func

def unsubscribe(func):
    """取消关注"""
    R("event", "unsubscribe", func)
    return func

def click(func):
    """点击事件"""
    R("event", "CLICK", func)
    return func


def text(func):
    """文本消息"""
    R("text", "all", func)
    return func

