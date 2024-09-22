import requests
import random
import base64
import time
from urlextract import URLExtract
import json
import re

__all__ = ['QrLogin','ClientkeyLogin']

class QrLogin():

    def __init__(self, url="qzone.qq.com", custom_data=None):
        """
        初始化对象,设置对应登录业务的s_url(u1)
        :param url: 登录url,留空默认使用QQ空间
        :param custom_data: 是否自定义登录数据,如需自定义需按照格式输入,否则从自带字典选取
        """
        app_list = {
            "qzone.qq.com":{"s_url":"https://qzs.qq.com/qzone/v5/loginsucc.html?para=izone","daid":"5","appid":"549000912"},
            "qun.qq.com":{"s_url":"https://qun.qq.com","daid":"73","appid":"715030901"},
            "vip.qq.com":{"s_url":"https://vip.qq.com/loginsuccess.html","daid":"18","appid":"8000201"}
        }
        if custom_data:
            data = custom_data
        else:
            data = app_list.get(url)
        self.s_url = data.get("s_url")
        self.daid = data.get("daid")
        self.appid = data.get("appid")
        self.qrsig = None
        self.ptqrtoken = None
        self.g_tk = None
        self.login_url = None

    def ptqrToken(self, qrsig) -> int:
        """
        计算ptqrtoken,需要qrsig
        :param qrsig: 获取二维码获得的qrsig
        :return: ptqrtoken
        """
        n, i, e = len(qrsig), 0, 0

        while n > i:
            e += (e << 5) + ord(qrsig[i])
            i += 1

        return 2147483647 & e

    def getQrcode(self, base64_encode=False) -> dict:
        """
        根据s_url获取二维码,返回以base64编码的qrcode图片(如果base64_encode为True,否则返回图片content),qrsig与ptqrtoken
        :return: qrsig,ptqrtoken
        """
        url = f"https://ssl.ptlogin2.qq.com/ptqrshow?appid={self.appid}&t={random.random()}&daid={self.daid}&pt_3rd_aid=0&u1={self.s_url}"
        qr_req = requests.get(url)
        qr_cookies = qr_req.cookies.get_dict()
        qrcode_content = qr_req.content
        if base64_encode:
            qrcode_content = base64.b64encode(qrcode_content)
        qrsig = qr_cookies.get("qrsig")
        ptqrtoken = self.ptqrToken(qrsig)
        self.qrsig = qrsig
        self.ptqrtoken = ptqrtoken
        if not (qrsig and ptqrtoken):
            return {"code":-1,"msg":"获取qrsig或ptqrtoken失败!"}
        return {"code":0,"msg":"获取成功!","img":qrcode_content,"qrsig":qrsig,"ptqrtoken":ptqrtoken}

    def check_scanning_status(self) -> dict:
        """
        检测二维码扫描状态,并返回QQ号和登录地址
        :return: 状态以及QQ号和登录网址
        """
        l = requests.get(
            f"https://ssl.ptlogin2.qq.com/ptqrlogin?u1={self.s_url}&ptqrtoken={self.ptqrtoken}&ptredirect=0&h=1&t=1&g=1&from_ui=1&ptlang=2052&action={time.time()}&js_ver=23111510&js_type=1&login_sig=&pt_uistyle=40&aid={self.appid}&daid={self.daid}&&o1vId=&pt_js_version=v1.48.1",
            cookies={"qrsig": self.qrsig})
        if '二维码未失效' in l.text:
            return {"code":0,"msg":"二维码未失效"}
        elif '二维码已失效' in l.text:
            return {"code":-1,"msg":"二维码已失效"}
        elif '二维码认证中' in l.text:
            return {"code":0,"msg":"二维码认证中"}
        elif '拒绝' in l.text:
            return {"code":-1,"msg":"用户已拒绝"}
        elif '成功' in l.text:
            uin = requests.utils.dict_from_cookiejar(l.cookies).get('uin')
            extractor = URLExtract()
            url = extractor.find_urls(l.text)[0]
            self.login_url = url
            return {"code":1,"msg":"登录成功","uin":uin,"login_url":url}
        else:
            return {"code":-2,"msg":"未知状态,请查阅return_msg!","return_msg":l.text}

    def getCookies(self) -> dict:
        """
        访问登录网址获取Cookies
        :return: Cookies
        """
        try:
            login_req = requests.get(self.login_url,allow_redirects=False)
            targetCookies = login_req.cookies.get_dict()
            return {"code":0,"msg":"获取成功!","cookies":targetCookies}
        except:
            return {"code":-1,"msg":"获取失败!"}

class ClientkeyLogin():

    def __init__(self):
        self.clientkey = None
        self.uin = None
        self.pt_local_token = None
        self.pt_login_sig = None
        self.session = requests.session()

    def getClientkey(self) -> dict:
        """
        获取Clientkey
        :return: QQ号,名称和clientkey
        """
        try:
            login_htm = self.session.get(
                "https://xui.ptlogin2.qq.com/cgi-bin/xlogin?s_url=https://qzs.qq.com/qzone/v5/loginsucc.html?para=izone")
            q_cookies = requests.utils.dict_from_cookiejar(login_htm.cookies)
            pt_local_token = q_cookies.get("pt_local_token")
            pt_login_sig = q_cookies.get("pt_login_sig")
            
            params = {"callback": "ptui_getuins_CB",
                      "r": "0.8987470931280881",
                      "pt_local_tk": pt_local_token}
            cookies = q_cookies
            headers = {"Referer": "https://xui.ptlogin2.qq.com/",
                       "Host": "localhost.ptlogin2.qq.com:4301",
                       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"}
            get_uin = self.session.get("https://localhost.ptlogin2.qq.com:4301/pt_get_uins", params=params, cookies=cookies,
                                  headers=headers).text
            uin_list = re.findall(r'\[([^\[\]]*)\]', get_uin)[0]
            split_list = list(map(lambda i: i if i[0] == '{' else '{' + i, uin_list.split(',{')))
            uin = None
            nickname = None
            if len(split_list) > 1:
                uin_list = json.loads(json.loads(json.dumps(split_list[0])))  # Json库我爱你loads后返回str还要再loads一次 凸(艹皿艹 )
                uin = uin_list.get("uin")
                nickname = uin_list.get("nickname")
            else:
                uin = json.loads(uin_list).get('uin')
                nickname = json.loads(uin_list).get('nickname')
            clientkey_params = {"clientuin": uin,
                                "r": "0.14246048393632815",
                                "pt_local_tk": pt_local_token,
                                "callback": "__jp0"}
            clientkey_get = self.session.get("https://localhost.ptlogin2.qq.com:4301/pt_get_st", cookies=cookies,
                                        headers=headers, params=clientkey_params)
            clientkey_cookies = requests.utils.dict_from_cookiejar(clientkey_get.cookies)
            clientkey = clientkey_cookies.get("clientkey")
            self.uin = uin
            self.clientkey = clientkey
            self.pt_local_token = pt_local_token
            self.pt_login_sig = pt_login_sig
            return {"code":0,"uin":uin,"nickname":nickname,"clientkey":clientkey}
        except Exception as e:
            return {"code":-1,"msg":repr(e)}
    def getLoginUrl(self) -> dict:
        """
        通过Clientkey获取登录url,包含ptsigx登录方式与QQ客户端登录方式对应的url
        :return: login_url
        """
        try:
            qzone_params = {
                "u1": "https://qzs.qq.com/qzone/v5/loginsucc.html?para=izone",
                "clientuin": self.uin,
                "pt_aid": "549000912",
                "keyindex": "19",
                "pt_local_tk": self.pt_local_token,
                "pt_3rd_aid": "0",
                "ptopt": "1",
                "style": "40",
                "daid": "5"
            }
            qzone_jump_cookies = {
                "clientkey": self.clientkey,
                "clientuin": str(self.uin),
                "pt_local_token": self.pt_local_token
            }
            headers = {"Referer": "https://xui.ptlogin2.qq.com/",
                       "Host": "ssl.ptlogin2.qq.com",
                       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"}
            qzone_url = self.session.get("https://ssl.ptlogin2.qq.com/jump", params=qzone_params, cookies=qzone_jump_cookies,
                                    headers=headers)
            extractor = URLExtract()
            qzone_url_ptsigx = extractor.find_urls(qzone_url.text)[0]
            qzone_url_cientkey = f"https://ssl.ptlogin2.qq.com/jump?ptlang=1033&clientuin={self.uin}&clientkey={self.clientkey}&u1=https://user.qzone.qq.com/{self.uin}/infocenter&keyindex=19"
            mail_params = {
                "u1": "https://graph.qq.com/oauth2.0/login_jump",
                "clientuin": self.uin,
                "pt_aid": "716027609",
                "keyindex": "19",
                "pt_local_tk": self.pt_local_token,
                "pt_3rd_aid": "102013353",
                "ptopt": "1",
                "style": "40",
                "daid": "383"
            }
            mail_cookies = {
                "clientkey": str(self.clientkey),
                "clientuin": str(self.uin),
                "pt_local_token": str(self.pt_local_token),
                "pt_login_sig": str(self.pt_login_sig)
            }
            mail_url = self.session.get("https://ssl.ptlogin2.qq.com/jump", params=mail_params, cookies=mail_cookies,
                                   headers=headers)
            mail_url_ptsigx = extractor.find_urls(mail_url.text)[0]
            mail_url_clientkey = f"https://ssl.ptlogin2.qq.com/jump?ptlang=1033&clientuin={self.uin}&clientkey={self.clientkey}&u1=https://wx.mail.qq.com/list/readtemplate?name=login_page.html&keyindex=19"
            qun_params = {
                "clientuin": str(self.uin),
                "keyindex": "19",
                "pt_aid": "715030901",
                "daid": "73",
                "u1": "https://qun.qq.com/",
                "pt_local_tk": str(self.pt_local_token),
                "pt_3rd_aid": "0",
                "ptopt": "1",
                "style": "40"
            }
            qun_cookies = {
                "clientkey": str(self.clientkey),
                "clientuin": str(self.uin),
                "pt_local_token": str(self.pt_local_token),
                "pt_login_sig": str(self.pt_login_sig)
            }
            qun_res = self.session.get("https://ssl.ptlogin2.qq.com/jump", params=qun_params, cookies=qun_cookies,
                                  headers=headers)
            qun_url_ptsigx = extractor.find_urls(qun_res.text)[0]
            return {"code":0,"msg":"获取成功!","ptsigx_url":{"qzone":qzone_url_ptsigx, "mail":mail_url_ptsigx, "qun":qun_url_ptsigx},"clientkey_url":{"qzone":qzone_url_cientkey,"mail":mail_url_clientkey}}
        except Exception as e:
            return {"code":-1,"msg":repr(e)}