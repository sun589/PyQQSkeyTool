# clientkey获取实例
import PyQQSkeyTool
ck = PyQQSkeyTool.ClientkeyLogin()
accounts = ck.getClientkey(port=4301)['data'] # 返回:{'code': 0, 'msg': '获取成功!', 'data': [{'clientkey': 'xxx', 'clientuin': 'xxx', 'nickname': 'xxx'},{'clientkey': 'xxx', 'clientuin': 'xxx', 'nickname': 'xxx'}.....]}
print(ck.getLoginUrl(uin=accounts[0]['clientuin'])) # 返回:{"code":0,"msg":"获取成功!",ptsigx_url:{xxx},clientkey_url:{xxx}}
# 你也可以这样写:
# print(ck.getLoginUrl(index=0))
# clientkey_url和ptsigx_url均可以登录网站,如果clientkey_url不行就换ptsigx_url的