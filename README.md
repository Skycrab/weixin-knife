# weixin-knife 微信开发利器---微信瑞士小刀


封装了微信的基础操作，demo使用了django，核心功能都在目录weixin下

demo django版本比较老(1.3.7), 抱歉抱歉


使用很方便, 很简单

    @HD.subscribe
    def subscribe(xml):
        """关注事件"""
        return "welcome to weixin-knife"

    @HD.unsubscribe
    def subscribe(xml):
        """取关事件"""
        print "leave weixin-knife"
        return "leave"


    @HD.text
    def text(xml):
        """文本消息"""
        content = xml.Content
        if content == "111":
            return {"Title":"美女", "Description":"比基尼美女", "PicUrl":"http://9smv.com/static/mm/uploads/150411/2-150411115450247.jpg", "Url":"http://9smv.com/beauty/list?category=5"}
        elif content == "222":
            return [
                ["比基尼美女", "比基尼美女", "http://9smv.com/static/mm/uploads/150411/2-150411115450247.jpg", "http://9smv.com/beauty/list?category=5"],
            ["长腿美女", "长腿美女", "http://9smv.com/static/mm/uploads/150506/2-150506111A9648.jpg", "http://9smv.com/beauty/list?category=8"]
            ]
        return "hello world"

    @sns_userinfo
    def oauth(request):
        """网页授权获取用户信息"""
        return HttpResponse(request.openid)


    新增jssdk(案列自定义分享), 微信支付，具体看demo
