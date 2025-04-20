import requests
import time
from urlextract import URLExtract

__all__ = [
    "login_by_clientkey"
]

def login_by_clientkey(uin:str, clientkey:str, which:int=0) -> str:
    """
    通过clientkey登录
    :param uin: 账号
    :param clientkey: clientkey
    :param which: 登录方式，0为QQ空间，1为QQ群，2为QQ邮箱，3为QQ会员，
                  4为微云，5为QQ账号中心，6为QQ秀，7为QQ恢复中心，
                  8为腾讯文档，9为QQ互联，10为腾讯IM
    :return: 登录网址
    """
    login_data = [
        {
            "proxy_url": "https://qzs.qq.com/qzone/v6/portal/proxy.html",
            "daid": "5",
            "hide_title_bar": "1",
            "low_login": "0",
            "qlogin_auto_login": "1",
            "no_verifyimg": "1",
            "link_target": "blank",
            "appid": "549000912",
            "style": "22",
            "target": "self",
            "s_url": "https://qzs.qq.com/qzone/v5/loginsucc.html?para=izone",
            "pt_qr_app": "手机QQ空间",
            "pt_qr_link": "https://z.qzone.com/download.html",
            "self_regurl": "https://qzs.qq.com/qzone/v6/reg/index.html",
            "pt_qr_help_link": "https://z.qzone.com/download.html",
            "pt_no_auth": "0"
        },
        {
            "pt_disable_pwd": "1",
            "appid": "715030901",
            "hide_close_icon": "1",
            "daid": "73",
            "pt_no_auth": "1",
            "s_url": "https://qun.qq.com/"
        },
        # {"u1":"https://wx.mail.qq.com/list/readtemplate?name=login_page.html","s_url":None},
        {
            "target": "self",
            "appid": "522005705",
            "daid": "4",
            "s_url": "https://wx.mail.qq.com/list/readtemplate?name=login_jump.html",
            "style": "25",
            "low_login": "1",
            "proxy_url": "https://mail.qq.com/proxy.html",
            "need_qr": "0",
            "hide_border": "1",
            "border_radius": "0",
            "self_regurl": "https://reg.mail.qq.com",
            "app_id": "11005?t=regist",
            "pt_feedback_link": "http://support.qq.com/discuss/350_1.shtml",
            "css": "https://res.mail.qq.com/zh_CN/htmledition/style/ptlogin_input_for_xmail.css",
            "enable_qlogin": "0"
        },
        {
            "appid": "8000201",
            "style": "20",
            "s_url": "https://vip.qq.com/loginsuccess.html",
            "maskOpacity": "60",
            "daid": "18",
            "target": "self"
        },
        # {"u1":"https://www.weiyun.com/?adtag=ntqqmainpanel","s_url":None},
        {
            "appid": "527020901",
            "daid": "372",
            "low_login": "0",
            "qlogin_auto_login": "1",
            "s_url": "https://www.weiyun.com/web/callback/common_qq_login_ok.html?login_succ",
            "style": "20",
            "hide_title": "1",
            "target": "self",
            "link_target": "blank",
            "hide_close_icon": "1",
            "pt_no_auth": "1"
        },
        {
            "style": "40",
            "appid": "1600001573",
            "s_url": "https://accounts.qq.com/homepage#/",
            "daid": "761",
            "hide_close_icon": "0"
        },
        {
            "appid": "10000101",
            "s_url": "https://qqshow.qq.com/manage/myCreation",
            "hide_close_icon": "1"
        },
        {
            "s_url": "https://huifu.qq.com/recovery/index.html?frag=1",
            "style": "20",
            "appid": "715021417",
            "daid": "768",
            "proxy_url": "https://huifu.qq.com/proxy.html"
        },
        {"u1": "https://docs.qq.com/desktop/?tdsourcetag=s_ntpcqq_panel_app", "s_url": None},
        {
            "daid": "377",
            "style": "11",
            "appid": "716027613",
            "target": "self",
            "pt_disable_pwd": "1",
            "s_url": "https://connect.qq.com/login_success.html",
            "t": str(time.time())
        },
        {
            "appid": "501038301",
            "target": "self",
            "s_url": "https://im.qq.com/loginSuccess"
        }
    ]
    session = requests.session()
    login_data = login_data[which]
    if login_data['s_url']:
        login_htm = session.get(
            "https://xui.ptlogin2.qq.com/cgi-bin/xlogin", params=login_data)
        q_cookies = requests.utils.dict_from_cookiejar(login_htm.cookies)
        pt_local_token = q_cookies.get("pt_local_token")
        headers = {"Referer": "https://xui.ptlogin2.qq.com/",
                   "Host": "ssl.ptlogin2.qq.com",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"}
        params = {
            "u1": login_data['s_url'],
            "clientuin": uin,
            "pt_aid": login_data['appid'],
            "keyindex": "19",
            "pt_local_tk": pt_local_token,
            "pt_3rd_aid": "0",
            "ptopt": "1",
            "style": "40"
        }
        if login_data.get("daid"): params['daid'] = login_data.get("daid")
        cookies = {
            "clientkey": clientkey,
            "clientuin": str(uin),
            "pt_local_token": pt_local_token
        }
        login_res = session.get("https://ssl.ptlogin2.qq.com/jump", params=params, cookies=cookies, headers=headers)
        extractor = URLExtract()
        login_url = extractor.find_urls(login_res.text)[0]
        return login_url
    else:
        return f"https://ssl.ptlogin2.qq.com/jump?ptlang=1033&clientuin={uin}&clientkey={clientkey}&u1={login_data['u1']}&keyindex=19"