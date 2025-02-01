import PyQQSkeyTool
import base64
import os
import time
qrlogin = PyQQSkeyTool.QrLogin("qzone.qq.com",custom_data=False) # 这里可以填qzone.qq.com/qun.qq.com/vip.qq.com/自定义(需往下看)
qr_data = qrlogin.getQrcode(base64_encode=True) # 返回:{"code":0,"img":"xxxxxx","qrsig":"xxxx","ptqrtoken"xxxxx"} 如果base64_encode为False则返回图片数据
code = qr_data.get("code")
if code != 0: # 代表获取失败
    raise Exception("获取失败!")
qr_img = qr_data.get("img")
qr_qrsig = qr_data.get("qrsig")
qr_ptqrtoken = qr_data.get("ptqrtoken")
with open("QRcode.jpg", 'wb') as f: # 写入至文件
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