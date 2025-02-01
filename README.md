****
# PyQQSkeyTool
一款集成了QQSkey/QQClientkey获取的库
****
## 安装方法
在cmd执行以下命令:  
```
pip install PyQQSkeyTool
```
****
# 版本要求
\>= 3.6
****
## 打包方法
在cmd执行以下命令:  
```
python setup.py sdist
```
****
## 使用实例
### 扫码登录:
``` python
# 扫码登录实例
import PyQQSkeyTool
import base64
import os
import time
qrlogin = PyQQSkeyTool.QrLogin("qzone.qq.com",custom_data=None) # 这里可以填qzone.qq.com/qun.qq.com/vip.qq.com/自定义(需往下看)
qr_data = qrlogin.getQrcode(base64_encode=True) # 返回:{"code":0,"img":"xxxxxx","qrsig":"xxxx","ptqrtoken"xxxxx"} 如果base64_encode为False则返回图片数据
code = qr_data.get("code")
if code != 0: # 代表获取失败
    raise Exception("获取失败!")
qr_img = qr_data.get("img")
qr_qrsig = qr_data.get("qrsig")
qr_ptqrtoken = qr_data.get("ptqrtoken")
with open("QRcode.jpg",'wb') as f: # 写入至文件
    f.write(base64.b64decode(qr_img)) # 如果前面base64_encode为False则直接f.write(qr_img)即可
os.startfile("QRcode.jpg") # 打开二维码
while True:
    status_data = qrlogin.check_scanning_status()
    if status_data.get("code") in [1, -1, -2]: # 检测登录成功或失效,成立则退出
        break
    print(time.strftime('%H:%M:%S'), status_data.get("msg")) # 输出二维码当前状态
    time.sleep(3) # 最好加个等待避免封ip,频率可自定
print(status_data.get("uin"), status_data.get("login_url")) # 输出QQ号和登录网址
print(qrlogin.getCookies()) # 输出Cookies 返回:{"code":0,msg:"获取成功!","cookies":{xxxxx}}
```
### 获取Clientkey:
``` python
# clientkey获取实例
import PyQQSkeyTool
ck = PyQQSkeyTool.ClientkeyLogin()
accounts = ck.getClientkey(port=4301)['data'] # 返回:{'code': 0, 'msg': '获取成功!', 'data': [{'clientkey': 'xxx', 'clientuin': 'xxx', 'nickname': 'xxx'},{'clientkey': 'xxx', 'clientuin': 'xxx', 'nickname': 'xxx'}.....]}
print(ck.getLoginUrl(uin=accounts[0]['uin'])) # 返回:{"code":0,"msg":"获取成功!",ptsigx_url:{xxx},clientkey_url:{xxx}}
# 你也可以这样写:
# print(ck.getLoginUrl(index=0))
# clientkey_url和ptsigx_url均可以登录网站,如果clientkey_url不行就换ptsigx_url的
```
更多例子请见仓库的[example](/example)文件夹
****
## 项目结构
```
│  .gitignore
│  LICENSE
│  README.md
│  setup.py
│          
├─example # 存放一些使用例子
│      control_qun.py # 控制群聊
│      control_qzone.py # 控制QQ空间
│      get_clientkey.py # 获取clientkey
│      QR_Login.py # 扫码登录
│      
└─PyQQSkeyTool # 项目主要代码
    │  api.py # 存放计算类的方法(如bkn,g_tk等)
    │  constant.py # 存放各种常量
    │  _core.py # 存放扫码和clientkey登录类
    │  __init__.py
    │  
    ├─client # 存放各种利用key操控的类
    │  │  qun.py
    │  │  qzone.py
    │  │  __init__.py
```
****
## 如何自定义登录data
库内已内置`qzone.qq.com`/`qun.qq.com`/`vip.qq.com`三个登录data,如需要其他请往下看:  
首先在你想要获取的网站开F12抓包,刷新登录页面,等待出现二维码,然后在开发工具点Img,找到
`https://ssl.ptlogin2.qq.com/ptqrshow`请求,点负载,然后将对应的参数填在指定格式的字典内:  
```
{"s_url":"xxxx","daid":"xxx","appid":"xxxx"}
```
s_url:对应参数的u1  
daid:对应参数的daid  
appid:对应参数的appid  
### 示例:  
![image](https://github.com/user-attachments/assets/47ccfbbb-0c45-45a0-b3ba-ab398101c0c2)
以上为`vip.qq.com`的参数,那么按照格式就应该在custom_data填入:  
```
{"s_url":"https://vip.qq.com/loginsuccess.html","daid":"18","appid":"8000201"}
```
在填好后,只需在实例化`QrLogin`类时填入参数custom_data即可生效使用
``` python
qrlogin = PyQQSkeyTool.QrLogin(custom_data={"s_url":"https://vip.qq.com/loginsuccess.html","daid":"18","appid":"8000201"})
