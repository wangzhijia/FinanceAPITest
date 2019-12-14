import re

from scripts.handle_mysql import HandleMysql
from scripts.handle_config import HandleConfig
from scripts.constants import USER_ACCOUNTS_FILE_PATH

class Context:
    """
    参数化
    """
    # 配置${not_exited_tel}的正则表达式
    not_exited_tel_pattern = re.compile(r'\$\{not_exited_tel\}')
    # 配置${invest_user_tel}的正则表达式
    invest_user_tel_pattern = re.compile(r'\$\{invest_user_tel\}')
    # 配置${loan_id}的正则表达式
    loan_id_pattern = re.compile(r'\$\{loan_id\}')

    handle_config = HandleConfig(USER_ACCOUNTS_FILE_PATH)

    @classmethod
    def not_exited_tel_replace(cls, data):
        """
        替换未注册的手机号
        :param data:
        :return:
        """
        do_mysql = HandleMysql()
        if re.search(cls.not_exited_tel_pattern,data):
            not_exited_tel = do_mysql.create_not_existed_mobile()
            data = re.sub(cls.not_exited_tel_pattern, not_exited_tel, data)
        do_mysql.close()
        return data

