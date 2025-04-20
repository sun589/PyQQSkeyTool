# 利用clientkey获取登录业务网站网址
import PyQQSkeyTool
ck = PyQQSkeyTool.ClientkeyLogin()
accounts = ck.getClientkey(port=4301)['data'] # 返回:{'code': 0, 'msg': '获取成功!', 'data': [{'clientkey': 'xxx', 'clientuin': 'xxx', 'nickname': 'xxx'},{'clientkey': 'xxx', 'clientuin': 'xxx', 'nickname': 'xxx'}.....]}
# print(ck.getLoginUrl(uin=accounts[0]['clientuin'])) # 返回:{"code":0,"msg":"获取成功!",ptsigx_url:{xxx},clientkey_url:{xxx}}
uin, clientkey = accounts[0]['clientuin'], accounts[0]['clientkey']
""""
which参数解释:
登录方式，0为QQ空间，1为QQ群，2为QQ邮箱，3为QQ会员，
4为微云，5为QQ账号中心，6为QQ秀，7为QQ恢复中心，
8为腾讯文档，9为QQ互联，10为腾讯IM
"""
url = PyQQSkeyTool.tool.login_by_clientkey(uin=uin, clientkey=clientkey, which=0)
print(url)