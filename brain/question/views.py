#coding=utf8

from django.shortcuts import HttpResponse, render_to_response, redirect

from .weixin import WeixinHelper
from .weixin import handler as HD


def do(request):
    """公众平台对接"""
    signature = request.REQUEST.get("signature", "")
    timestamp = request.REQUEST.get("timestamp", "")
    nonce = request.REQUEST.get("nonce", "")
    if not any([signature, timestamp, nonce]) or not WeixinHelper.checkSignature(signature, timestamp, nonce):
        return HttpResponse("")

    if request.method == "GET":
        return HttpResponse(request.GET.get("echostr"))
    elif request.method == "POST":
        handler = HD.MessageHandle(request.raw_post_data)
        response = handler.start()
        return HttpResponse(response)
    else:
        return HttpResponse("")


@HD.subscribe
def subscribe(xml):
    return "welcome to brain"

@HD.unsubscribe
def subscribe(xml):
    print "leave"
    return "leave  brain"


@HD.text
def text(xml):
    content = xml.Content
    if content == "111":
        return {"Title":"美女", "Description":"比基尼美女", "PicUrl":"http://9smv.com/static/mm/uploads/150411/2-150411115450247.jpg", "Url":"http://9smv.com/beauty/list?category=5"}
    elif content == "222":
        return [
            ["比基尼美女", "比基尼美女", "http://9smv.com/static/mm/uploads/150411/2-150411115450247.jpg", "http://9smv.com/beauty/list?category=5"],
            ["长腿美女", "长腿美女", "http://9smv.com/static/mm/uploads/150506/2-150506111A9648.jpg", "http://9smv.com/beauty/list?category=8"]
        ]
    return "hello world"








