import http.client
import urllib.parse

from wxpy import *

# 服务地址
from config import platform_name, Config

sms_host = "sms.yunpian.com"
voice_host = "voice.yunpian.com"
# 端口号
port = 443
# 版本号
version = "v2"
# 模板短信接口的URI
sms_tpl_send_uri = "/" + version + "/sms/tpl_single_send.json"


def tpl_send_sms(apikey, tpl_id, tpl_value, mobile):
    """
    模板接口发短信
    """
    params = urllib.parse.urlencode({
        'apikey': apikey,
        'tpl_id': tpl_id,
        'tpl_value': urllib.parse.urlencode(tpl_value),
        'mobile': mobile
    })
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"
    }
    conn = http.client.HTTPSConnection(sms_host, port=port, timeout=30)
    conn.request("POST", sms_tpl_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str


def send_voice_sms(apikey, code, mobile):
    """
    通用接口发短信
    """
    params = urllib.parse.urlencode({'apikey': apikey, 'code': code, 'mobile': mobile})
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"
    }
    sms_voice_send_uri = "/" + version + "/voice/send.json"

    conn = http.client.HTTPSConnection(voice_host, port=port, timeout=30)
    conn.request("POST", sms_voice_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str


class Info(object):
    def __init__(self, apikey=Config.apikey, wechat_info=False):
        self.apikey = apikey
        self.init(wechat_info)

    def init(self, wechat_info):
        if wechat_info:
            if platform_name == "Linux":
                self.bot = Bot(cache_path=True, console_qr=True)
            else:
                self.bot = Bot(cache_path=True)

    def info_person(self):
        """
        给相关人员元发通知
        """
        phone = ""
        code = 4444
        apikey = self.apikey
        send_voice_sms(apikey, code, phone)

    def info_wechat(self, info_str):
        """
        发送微信通知
        :param info_str:
        :return:
        """
        person = ensure_one(self.bot.friends().search("robot"))
        group = ensure_one(self.bot.groups().search("5410"))
        person.send(info_str)

    def info_wsg(self):
        """
         给指定人发通知,打电话提示
        :return: bool
        """
        # IFTTT
        apikey = ""  # wsg
        # 语音通知
        voiceCode = "1111"
        mobile_phone = ""
        send_voice_sms(apikey, voiceCode, mobile_phone)
        print("333")
        # 短信通知
        tpl_id = "2742926"
        tpl_value = "【wsg】#info#，请登录选课页面查看选课结果。"  # info为可替换变量，不超过12字
        tpl_id = "2742946"
        tpl_value = "【wsg】#app#程序异常，error：#error#，请登录服务器查看。"  # app,error为可替换变量，加起来不超12字
        tpl_send_sms(apikey, tpl_id, tpl_value, mobile_phone)
