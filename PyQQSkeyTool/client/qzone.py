import requests
from ..api import *
import json

__all__ = ["QzoneManager"]

class QzoneManager:

    def __init__(self, uin:str, skey:str, p_skey:str):
        self.uin = 'o' + uin if uin[0] != 'o' else uin
        self.skey = skey
        self.p_skey = p_skey
        self.g_tk = g_tk(p_skey)
        self.cookies = {
            "p_skey": p_skey,
            "uin": uin,
            "skey": skey,
            "p_uin": uin
        }
        self.headers = {
            "Referer": f"https://user.qzone.qq.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
            "Origin": "https://user.qzone.qq.com"
        }

    def change_name(self, name:str):
        """
        修改昵称
        :param name: 要改的昵称
        :return: api返回的结果
        """
        data = {
    "nickname":name,
    "emoji":"",
    "sex":"1",
    "birthday":"1900-1-1",
    "province":"44",
    "city":"0",
    "country":"1",
    "marriage":"0",
    "bloodtype":"5",
    "hp":"0",
    "hc":"0",
    "hco":"0",
    "career":"",
    "company":"",
    "cp":"0",
    "cc":"0",
    "cb":"",
    "cco":"0",
    "lover":"",
    "islunar":"0",
    "mb":"1",
    "uin":f"{self.uin[1:]}",
    "pageindex":"1",
    "fupdate":"1",
    "qzreferrer":"https://user.qzone.qq.com/proxy/domain/qzs.qq.com/qzone/v6/setting/profile/profile.html?tab=base",
    "g_iframeUser":"1"
}
        r1 = requests.post(
            f"https://h5.qzone.qq.com/proxy/domain/w.qzone.qq.com/cgi-bin/user/cgi_apply_updateuserinfo_new?&g_tk={self.g_tk}",
            data=data, headers=self.headers, params=data, cookies=self.cookies)
        r1.encoding = 'utf-8'
        return r1.text
    def get_friends_list(self) -> list:
        """
        获取好友列表
        :return: 好友列表
        """
        data = {
    "uin":self.uin[1:],
    "do":"1",
    "rd":f"0.928374978349",
    "fupdate":"1",
    "clean":"1",
    "g_tk":self.g_tk
}
        friends = []
        try:
            res = requests.get("https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_ship_manager.cgi",params=data,cookies=self.cookies,headers=self.headers,json=data,data=data)
            res.encoding = 'utf-8'
            res = res.text[10:-2]
            friend_list = json.loads(res).get("data").get("items_list")
            print(friend_list)
        except Exception as e:
            return [repr(e)]
        for i in friend_list:
            friends.append({
                'name':i['name'],
                'uin':str(i['uin']),
                'img':i['img']
            })
        return friends

    def publish_emotion(self, content:str):
        """
        发表说说
        :param content: 说说的内容
        :return: api返回的结果
        """
        data = {
    "syn_tweet_verson":"1",
    "paramstr":"1",
    "pic_template":"",
    "richtype":"",
    "richval":"",
    "special_url":"",
    "subrichtype":"",
    "who":"1",
    "con":content,
    "feedversion":"1",
    "ver":"1",
    "ugc_right":"1",
    "to_sign":"0",
    "hostuin":self.uin[1:],
    "code_version":"1",
    "format":"fs",
    "qzreferrer":f"https://user.qzone.qq.com/{self.uin[1:]}"
}
        r1 = requests.post(f"https://user.qzone.qq.com/proxy/domain/taotao.qzone.qq.com/cgi-bin/emotion_cgi_publish_v6?&g_tk={self.g_tk}", data=data,headers=self.headers,params=data,cookies=self.cookies).text
        r1.encoding = 'utf-8'
        return r1

    def get_emotions_list(self, page=0, num:int=1, replace_newline:str='\n') -> list:
        """
        获取说说
        :param page: 页数,默认0
        :param num: 获取数量,需为int,默认1
        :param replace_newline: 指定替换换行符的内容
        :return: 说说
        """
        data = {
    "uin":self.uin[1:],
    "inCharset":"utf-8",
    "outCharset":"utf-8",
    "hostUin":self.uin[1:],
    "notice":"0",
    "sort":"0",
    "pos":str(page),
    "num":str(num),
    "cgi_host":"https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6",
    "code_version":"1",
    "format":"json",
    "need_private_comment":"1",
    "g_tk":self.g_tk
}
        count = 0
        emotions_list = []
        while True:
            res = requests.get(
                f"https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6",
                params=data, headers=self.headers, cookies=self.cookies)
            res.encoding = 'utf-8'
            res = res.json()
            if res.get("msglist"):
                msg_list = res['msglist']
                for msg in msg_list:
                    if count >= num:
                        return emotions_list
                    _ = {
                        "content":msg.get("content").replace("\n",replace_newline),
                        "createtime":msg.get("createTime"),
                        "tid":msg.get("tid"),
                        "img_url": msg['pic'][0]['url1'] if msg.get("pic") else None,
                        "video_url": msg['video'][0]['url3'] if msg.get("video") else None,
                    }
                    if _ in emotions_list:
                        continue
                    emotions_list.append(_)
                    count += 1
                data['pos'] = str(int(data['pos'])+1)
            else:
                break
        return emotions_list

    def delete_emotion(self, tid:str):
        """
        删除说说
        :param tid: 说说的tid
        :return: api返回的结果
        """
        data = {
    "hostuin":self.uin[1:],
    "tid":tid,
    "t1_source":"1",
    "code_version":"1",
    "format":"fs",
    "qzreferrer":f"https://user.qzone.qq.com/{self.uin[1:]}"
}
        return requests.post(f"https://user.qzone.qq.com/proxy/domain/taotao.qzone.qq.com/cgi-bin/emotion_cgi_delete_v6?&g_tk={self.g_tk}",json=data,data=data,cookies=self.cookies,headers=self.headers).text
