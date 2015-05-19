#coding=utf8
import time
from django.shortcuts import HttpResponse, render_to_response, redirect

from weixin import handler as HD
from weixin.backends.dj import Helper, sns_userinfo
from weixin import WeixinHelper, JsApi_pub, WxPayConf_pub, UnifiedOrder_pub, Notify_pub, catch



def do(request):
    """公众平台对接"""
    signature = request.REQUEST.get("signature", "")
    timestamp = request.REQUEST.get("timestamp", "")
    nonce = request.REQUEST.get("nonce", "")
    if not any([signature, timestamp, nonce]) or not WeixinHelper.checkSignature(signature, timestamp, nonce):
        return HttpResponse("check failed")

    if request.method == "GET":
        return HttpResponse(request.GET.get("echostr"))
    elif request.method == "POST":
        #print request.raw_post_data
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
    elif content == "push":
        Helper.send_text_message(xml.FromUserName, "推送消息测试")
        return "push ok"

    return "hello world"

@sns_userinfo
def oauth(request):
    """网页授权获取用户信息"""
    resp = HttpResponse(request.openid)
    resp.set_cookie("openid", Helper.sign_cookie(request.openid))
    return resp



def share(request):
    """jssdk 分享"""
    url = "http://"+request.get_host() + request.path
    sign = Helper.jsapi_sign(url)
    sign["appId"] = WxPayConf_pub.APPID
    return render_to_response("share.html", {"jsapi":sign})

@sns_userinfo
def pay(request):
    response = render_to_response("pay.html")
    response.set_cookie("openid", Helper.sign_cookie(request.openid))
    return response

@sns_userinfo
@catch
def paydetail(request):
    """获取支付信息"""
    openid = request.openid
    money = request.POST.get("money") or "0.01"
    money = int(float(money)*100)

    jsApi = JsApi_pub()
    unifiedOrder = UnifiedOrder_pub()
    unifiedOrder.setParameter("openid",openid) #商品描述
    unifiedOrder.setParameter("body","充值测试") #商品描述
    timeStamp = time.time()
    out_trade_no = "{0}{1}".format(WxPayConf_pub.APPID, int(timeStamp*100))
    unifiedOrder.setParameter("out_trade_no", out_trade_no) #商户订单号
    unifiedOrder.setParameter("total_fee", str(money)) #总金额
    unifiedOrder.setParameter("notify_url", WxPayConf_pub.NOTIFY_URL) #通知地址 
    unifiedOrder.setParameter("trade_type", "JSAPI") #交易类型
    unifiedOrder.setParameter("attach", "6666") #附件数据，可分辨不同商家(string(127))
    try:
        prepay_id = unifiedOrder.getPrepayId()
        jsApi.setPrepayId(prepay_id)
        jsApiParameters = jsApi.getParameters()
    except Exception as e:
        print(e)
    else:
        print jsApiParameters
        return HttpResponse(jsApiParameters)


FAIL, SUCCESS = "FAIL", "SUCCESS"
@catch
def payback(request):
    """支付回调"""
    xml = request.raw_post_data
    #使用通用通知接口
    notify = Notify_pub()
    notify.saveData(xml)
    print xml
    #验证签名，并回应微信。
    #对后台通知交互时，如果微信收到商户的应答不是成功或超时，微信认为通知失败，
    #微信会通过一定的策略（如30分钟共8次）定期重新发起通知，
    #尽可能提高通知的成功率，但微信不保证通知最终能成功
    if not notify.checkSign():
        notify.setReturnParameter("return_code", FAIL) #返回状态码
        notify.setReturnParameter("return_msg", "签名失败") #返回信息
    else:
        result = notify.getData()

        if result["return_code"] == FAIL:
            notify.setReturnParameter("return_code", FAIL)
            notify.setReturnParameter("return_msg", "通信错误")
        elif result["result_code"] == FAIL:
            notify.setReturnParameter("return_code", FAIL)
            notify.setReturnParameter("return_msg", result["err_code_des"])
        else:
            notify.setReturnParameter("return_code", SUCCESS)
            out_trade_no = result["out_trade_no"] #商户系统的订单号，与请求一致。
            ###检查订单号是否已存在,以及业务代码(业务代码注意重入问题)

    return  HttpResponse(notify.returnXml())
















