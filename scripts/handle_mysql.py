import random

import pymysql

from scripts.handle_config import do_config


class HandleMysql:
    """
    处理mysql
    """
    def __init__(self):
        self.conn = pymysql.connect(host=do_config("mysql","host"),
                                    user=do_config("mysql","user"),
                                    password=do_config("mysql","password"),
                                    db=do_config("mysql","db"),
                                    port=do_config("mysql","port"),
                                    charset=do_config("mysql","charset"),
                                    cursorclass=pymysql.cursors.DictCursor)

        self.cursor = self.conn.cursor()

    def get_one_value(self, sql, arg=None):
        """
        获取单个值
        :param sql:
        :param arg:
        :return:
        """
        self.cursor.execute(sql, arg)
        self.conn.commit()
        return self.cursor.fetchone()

    def get_values(self, sql, arg=None):
        """
        获取多个值
        :param sql:
        :param arg:
        :return:
        """
        self.cursor.execute(sql, arg)
        self.conn.commit()

        return self.cursor.fetchall()

    def __call__(self, sql, arg=None, is_more=True):
        """

        :param sql:
        :param arg:
        :param is_more:
        :return:
        """
        self.cursor.execute(sql, arg)
        self.conn.commit()

        if is_more:
            result = self.cursor.fetchone()
        else:
            result = self.cursor.fetchall()

        return result

    @staticmethod
    def create_mobile():
        """
        随机生成11位手机号
        :return:
        """
        start_mobile = ['130','131','132','133','134','135','136','137','138','139',
                        '150','151','152','153','155','156','157','158','159',
                        '180','181','182','183','184','185','186','187','188','189']
        start_num = random.choice(start_mobile)
        one_str = '0123456789'
        end_num = "".join(random.sample(one_str,8))
        return start_num + end_num

    def is_existed_mobile(self, mobile):
        """

        :param mobile:
        :return:
        """
        sql = "select `MobilePhone` from future.`member` where `MobilePhone`=%s"
        if self(sql, arg=(mobile,)):
            return True
        else:
            return False

    def create_not_existed_mobile(self):
        """

        :return:
        """
        while True:
            one_mobile = self.create_mobile()
            if not self.is_existed_mobile(one_mobile):
                break
        return one_mobile

    def close(self):
        """
        关闭连接
        :return:
        """
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    sql_1 = "select * from `member` limit 0,10;"
    sql_2 = "select * from `member` where LeaveAmount > %s limit 0,10;"
    do_mysql = HandleMysql()
    result1 = do_mysql(sql=sql_1)
    print(do_mysql(sql=sql_2, arg=(600,)))
    do_mysql.close()
    pass

