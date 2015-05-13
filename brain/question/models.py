#coding=utf8

from django.db import models

# Create your models here.

class User(models.Model):
    """玩家信息"""
    openid = models.CharField(max_length=64,verbose_name="OPEN ID",unique = True)
    name = models.CharField(max_length=30,verbose_name="用户名称",default="")
    headimgurl = models.URLField(max_length=255,verbose_name="用户头像",default="")
    sex = models.IntegerField(max_length=2,verbose_name="用户性别1男2女0未知",default=0)
    brain = models.IntegerField(max_length=11,verbose_name="智商",default=0)
    level = models.IntegerField(max_length=11,verbose_name="等级",default=1)
    gold = models.IntegerField(max_length=11,verbose_name="砖石",default=0)
    city = models.CharField(max_length=64,verbose_name="城市",default="")
    province = models.CharField(max_length=64,verbose_name="省份",default="")
    country = models.CharField(max_length=64,verbose_name="国家",default="")
    last_login = models.IntegerField(max_length=11,verbose_name="上次登录")



class Friend(models.Model):
    """好友"""
    user = models.ForeignKey(User, verbose_name="主人")
    friend = models.CharField(max_length=2014, verbose_name="好友id列表") #','分割


class Category(models.Model):
    """题目分类"""
    name = models.CharField(max_length=30,verbose_name="分类名")
    parent = models.ForeignKey('self', blank=True, null=True, related_name="children")

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = "分类"
        ordering = ('id',)

    def __unicode__(self):
        return self.name

    def child_list(self):
        """获取该分类下所有分类"""
        categorys = self.children.all()
        return categorys

    @classmethod
    def first_category(cls):
        """一级分类"""
        categorys = Category.objects.filter(parent=None)
        return categorys


class Question(models.Model):
    """问答题目"""


class Action(models.Model):
    """操作集合"""
    name = models.CharField(max_length=30,verbose_name="动作名称")



class Props(models.Model):
    """游戏道具"""
    name = models.CharField(max_length=30,verbose_name="道具名")
    desc = models.CharField(max_length=1023,verbose_name="描述")


class Announcement(models.Model):
    """公告"""
    title = models.CharField(max_length=30, verbose_name="标题")
    content = models.CharField(max_length=65535, verbose_name="内容")
    begin_time = models.IntegerField(max_length=11, verbose_name="开始时间")
    end_time = models.IntegerField(max_length=11, verbose_name="结束时间")


class Activity(models.Model):
    """活动"""
    title = models.CharField(max_length=30, verbose_name="标题")



class Task(models.Model):
    """任务"""
    name = models.CharField(max_length=64, verbose_name="任务名")
    count = models.IntegerField(max_length=4, verbose_name="完成次数")
    reward = models.CharField(max_length=128, verbose_name="奖励") #奖励：1.2倍经验卡*1
    formula = models.CharField(max_length=1024, verbose_name="奖励公式") #直接挂钩游戏道具id



class DailyTask(models.Model):
    """用户每日任务完成记录"""
    user = models.ForeignKey(User, verbose_name="用户")
    value = models.CharField(max_length=1024, verbose_name="完成状态")  #json格式编码


class Shop(models.Model):
    """商城"""
    props = models.ForeignKey(Props, verbose_name="道具")
    count = models.IntegerField(max_length=11, verbose_name="数量")
    cost = models.IntegerField(max_length=11, verbose_name="花费砖石数量")
    desc = models.CharField(max_length=128, verbose_name="物品说明") #单局经验*2


class Package(models.Model):
    """背包"""
    user = models.ForeignKey(User, verbose_name="用户")
    value = models.CharField(max_length=1024, verbose_name="背包信息")  #json格式编码



class PayDiscount(models.Model):
    """充值折扣"""
    count = models.IntegerField(max_length=11, verbose_name="砖石数量")
    discount = models.IntegerField(max_length=11, verbose_name="赠送数量")
    cost = models.IntegerField(max_length=11, verbose_name="花费ＲＭＢ")


class Mail(models.Model):
    """邮件"""
    sender = models.IntegerField(max_length=11, verbose_name="发送方")
    receiver = models.IntegerField(max_length=11, verbose_name="接收方")
    content = models.CharField(max_length=2048, verbose_name="内容")
    reward = models.CharField(max_length=128, verbose_name="奖励") #奖励：1.2倍经验卡*1
    formula = models.CharField(max_length=1024, verbose_name="奖励公式") #直接挂钩游戏道具id



















