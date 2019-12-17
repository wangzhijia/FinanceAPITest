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

    @classmethod
    def invest_user_tel_replace(cls, data):
        """
        替换投资人的手机号
        :param data:
        :return:
        """
        if re.search(cls.invest_user_tel_pattern, data):
            invest_user_tel = str(cls.handle_config("invest_user", "mobilephone"))
            data = re.sub(cls.invest_user_tel_pattern, invest_user_tel, data)
        return data

    @classmethod
    def loan_id_replace(cls, data):
        """

        :param data:
        :return:
        """
        if re.search(cls.loan_id_pattern, data):
            load_id = str(getattr(cls, "load_id"))
            data = re.sub(cls.loan_id_pattern, load_id, data)
        return data

    @classmethod
    def register_parameterization(cls, data):
        """
        实现注册功能的参数化
        :param data:
        :return:
        """
        data = cls.not_exited_tel_replace(data)
        data = cls.invest_user_tel_replace(data)
        return data

    @classmethod
    def recharge_parameterization(cls, data):
        pass

    @classmethod
    def invest_parameterization(cls, data):
        data = cls.loan_id_replace(data)
        return data


if __name__ == '__main__':
    target_str5 = '{"mobilephone":"${invest_user_tel}","pwd":"123456","regname":"KeYou"}'
    one_context = Context
    print(one_context.register_parameterization(target_str5))
    pass
