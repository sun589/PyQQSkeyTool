import requests
import re

__all__ = [
    "get_avatar_url",
    "get_nickname"
]

def get_avatar_url(uin:str, size:int=100) -> str:
    """
    获取QQ头像URL
    :param uin: QQ号
    :param size: 头像大小，默认为100像素，可选值为40、100、140、640
    :return: 头像URL
    """
    return f"https://q1.qlogo.cn/g?b=qq&nk={uin}&s={size}"

def get_nickname(uin:str) -> tuple:
    """
    获取QQ昵称
    :param uin: QQ号
    :return: 昵称与api返回的原始信息
    """
    get_nickname_req = requests.get(f'https://users.qzone.qq.com/fcg-bin/cgi_get_portrait.fcg?uins={uins[i]}')
    get_nickname_req.encoding = 'utf-8'
    name = re.findall(r'\[.*,.*,.*,.*,.*,.*,"(.*)",.*\]', get_nickname_req.text)[0]
    return name, get_nickname_req.text