# QQ空间操控实例
import PyQQSkeyTool
qzone_client = PyQQSkeyTool.client.QzoneManager(uin="xxx",skey="xxx",p_skey="xxx")
print(qzone_client.g_tk)
print(qzone_client.get_friends_list())
print(qzone_client.publish_emotion(content="test"))
print(qzone_client.get_emotions_list(page=0,num=1))
print(qzone_client.delete_emotion(tid="xxx"))
# 以下为已失效的功能
# print(qzone_client.change_name("xxx"))
