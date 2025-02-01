# QQ群操作实例
import PyQQSkeyTool
qun_client = PyQQSkeyTool.client.QunManager(uin="xxx",skey="xxx",p_skey="xxx")
print(qun_client.bkn)
print(qun_client.get_qun_members(target_qid="xxx"))
print(qun_client.add_qun_notice(content="xxx",
                                target_qid="xxx",
                                pinned=1,
                                confirm_required=1,
                                to_json=True))
print(qun_client.delete_notice(target_qid="xxx",fid="xxx"))
print(qun_client.get_notices_list(target_qid="xxx",replace_newline="[换行]"))
