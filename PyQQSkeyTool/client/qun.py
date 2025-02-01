import requests
from ..api import *
from html import unescape

__all__ = ["QunManager"]

class QunManager:

    __slots__ = ['uin', 'skey', 'p_skey', 'bkn', 'cookies', 'headers']

    def __init__(self, uin, skey:str, p_skey:str):
        self.uin = str(uin)
        self.skey = skey
        self.p_skey = p_skey
        self.bkn = bkn(skey)
        self.cookies = {
            "p_skey": self.p_skey,
            "uin": self.uin,
            "skey": self.skey,
            "p_uin": self.uin,
            "ptui_loginuin":str(uin)
        }
        self.headers = {
            "Referer": "https://web.qun.qq.com/mannounce/index.html?_wv=1031&_bid=148",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; MI 8 Build/QKQ1.190910.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/109.0.5414.86 MQQBrowser/6.2 TBS/046715 Mobile Safari/537.36 V1_AND_SQ_8.9.78_4548_YYB_D QQ/8.9.78.12275 NetType/WIFI WebP/0.3.0 AppId/537175315 Pixel/1080 StatusBarHeight/82 SimpleUISwitch/0 QQTheme/2099 StudyMode/0 CurrentMode/0 CurrentFontScale/1.0 GlobalDensityScale/0.9818182 AllowLandscape/false InMagicWin/0",
            "Host": "web.qun.qq.com",
            "Origin": "https://web.qun.qq.com"
        }

    def add_qun_notice(self, content:str, target_qid, pinned:int=0, confirm_required:int=0, to_json:bool=False):
        """
        发送群公告，需要提供详细参数
        :param content: 公告内容
        :param target_qid: 目标群号
        :param pinned: 是否置顶,默认0(不需要)
        :param confirm_required: 是否需要确定收到,默认0(不需要)
        :param to_json: 是否转为json，默认False
        :return: api所返回的内容
        """
        data = {
            "qid": target_qid,
            "bkn": self.bkn,
            "text": content,
            "pinned": pinned,
            "type": 1,
            "settings": {"is_show_edit_card": 1, "tip_window_type": 0, "confirm_required": confirm_required}
        }
        r1 = requests.post(f"https://web.qun.qq.com/cgi-bin/announce/add_qun_notice?bkn={self.bkn}", params=data,headers=self.headers, cookies=self.cookies)
        return r1.json() if to_json else r1.text

    def get_notices_list(self, target_qid, replace_newline:str='\n') -> list:
        """
        获取群公告
        :param target_qid: 目标群号
        :param replace_newline: 指定替换换行字符的内容,默认\n
        :return: 以json为格式的群公告列表
        """
        data = {
            "qid": target_qid,
            "bkn": self.bkn,
            "n":"10",
            "s":"-1",
            "ni":"1",
            "i":"1",
            "ft":"23"
        }
        notices = []
        while True:
            res = requests.post(f"https://web.qun.qq.com/cgi-bin/announce/list_announce?bkn={self.bkn}", params=data,json=data,headers=self.headers, cookies=self.cookies).json()
            if "feeds" in res or "inst" in res:
                data['s'] = str(int(data['s'])-10)
                data['ni'] = 'undefined'
                try:
                    for j in res['inst']:
                        _ = {
                            'uin':j['u'],
                            'fid':j['fid'],
                            'content':unescape(j['msg']['text']).replace("\n",replace_newline)
                        }
                        if _ in notices:
                            break
                        notices.append(_)
                except:
                    pass
                try:
                    for j in res['feeds']:
                        _ = {
                            'uin':j['u'],
                            'fid':j['fid'],
                            'content':unescape(j['msg']['text']).replace("\n",replace_newline)
                        }
                        if _ in notices:
                            break
                        notices.append(_)
                except:
                    pass
            else:
                break
        return notices

    def delete_notice(self, target_qid, fid:str, to_json:bool=False) -> dict:
        """
        删除群公告，需要fid，可通过get_notices_list获取
        :param target_qid: 目标群号
        :param fid: 对应公告的fid
        :param to_json: 是否转为json，默认False
        :return: api返回的结果
        """
        data = {
            "qid": target_qid,
            "bkn": self.bkn,
            "fid": fid
        }
        r1 = requests.post(f"https://web.qun.qq.com/cgi-bin/announce/del_feed?bkn={bkn}", data=data,params=data,headers=self.headers, cookies=self.cookies)
        return r1.json() if to_json else r1.text

    def get_qun_members(self, target_qid) -> list:
        """
        获取群成员列表
        :param target_qid: 目标群号
        :return: 群成员列表
        """
        data = {
            "st":"0",
            "start":"0",
            "end":"9",
            "sort":"1",
            "group_id":target_qid,
            "gc":target_qid
        }
        l = []
        start = 0
        end = 9
        while True:
            res = requests.post(f"https://qun.qq.com/cgi-bin/qun_mgr/search_group_members?bkn={self.bkn}&ts=1702901784527",cookies=self.cookies,data=data,headers=self.headers).json()
            try:
                for i in res['mems']:
                    _ = {
                        'uin': i['uin'],
                        'nickname': i['nick'],
                        'join_time': i['join_time'],
                        'last_speak_time': i['last_speak_time']
                    }
                    if _ in l:
                        break
                    l.append(_)
                start += 10
                end += 10
                data['start'],data['end'] = str(start),str(end)
            except:
                break
        return l