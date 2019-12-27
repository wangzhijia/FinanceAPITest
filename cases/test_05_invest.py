import unittest

from libs.ddt import ddt,data

from scripts.handle_excel import HandleExcel
from scripts.handle_config import do_config
from scripts.handle_log import HandleLog
from scripts.handle_request import HttpRequest
from scripts.handle_mysql import HandleMysql
from scripts.handle_context import Context
from scripts.constants import TEST_DATAS_FILE_PATH

do_excel = HandleExcel(TEST_DATAS_FILE_PATH, "invest")
do_log = HandleLog().get_logger()


@ddt
class TestInvest(unittest.TestCase):
    """
    测试投资功能
    """
    cases = do_excel.get_cases()

    @classmethod
    def setUpClass(cls):
        cls.send_request = HttpRequest()
        cls.handle_mysql = HandleMysql()
        do_log.info("\n{:=^40s}".format("开始执行投资功能测试"))

    @classmethod
    def tearDownClass(cls):
        cls.send_request.close()
        cls.handle_mysql.close()
        do_log.info("\n{:=^40s}".format("投资功能测试用例执行结束"))

    @data(*cases)
    def test_invest(self,data_namedtuple):
        """
        测试投资功能
        :param data_namedtuple:
        :return:
        """
        run_success_msg = do_config("msg", "success_result")
        run_fail_msg = do_config("msg", "fail_result")

        new_data = Context.invest_parameterization(data_namedtuple.data)

        new_url = do_config("api", "prefix_url") + data_namedtuple.url

        response = self.send_request(method=data_namedtuple.method, url=new_url, data=new_data)
        try:
            self.assertEqual(200, response.status_code, msg="测试【{}】时，请求失败！状态码为【{}】"
                             .format(data_namedtuple.title, response.status_code))

        except AssertionError as e:
            do_log.error("具体异常为：{}".format(e))
            raise e

        if response.json().get("msg") == "加标成功":
            check_sql = data_namedtuple.check_sql
            if check_sql:
                check_sql = Context.invest_parameterization(check_sql)
                mysql_data = self.handle_mysql(sql=check_sql)
                Context.load_id = mysql_data.get("Id")

        code = response.json().get("code")

        try:
            self.assertEqual(str(data_namedtuple.expected), code, msg="测试【{}】失败"
                             .format(data_namedtuple.title))

        except AssertionError as e:
            do_log.error("具体异常为：{}".format(e))
            do_excel.write_result(row=data_namedtuple.case_id+1, actual=response.text, result=run_fail_msg)
            raise e
        else:
            do_excel.write_result(row=data_namedtuple.case_id + 1, actual=response.text, result=run_success_msg)


if __name__ == '__main__':
    unittest.main()





