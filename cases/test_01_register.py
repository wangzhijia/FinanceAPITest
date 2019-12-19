import unittest

from libs.ddt import ddt, data

from scripts.handle_excel import HandleExcel
from scripts.handle_config import do_config
from scripts.handle_log import HandleLog
from scripts.handle_request import HttpRequest
from scripts.handle_context import Context
from scripts.constants import TEST_DATAS_FILE_PATH

do_excel = HandleExcel(TEST_DATAS_FILE_PATH, "register")
do_log = HandleLog().get_logger()


@ddt
class TestRegister(unittest.TestCase):
    """
    测试注册功能
    """
    cases = do_excel.get_cases()

    @classmethod
    def setUpClass(cls):
        """

        :return:
        """
        cls.send_request = HttpRequest()
        do_log.info("\n{:=^40s}".format("开始执行注册功能用例"))

    @classmethod
    def tearDownClass(cls):
        """

        :return:
        """
        cls.send_request.close()
        do_log.info("\n{:=^40s}".format("注册功能用例执行结束"))

    @data(*cases)
    def test_register(self, data_namedtuple):
        """

        :param data_namedtuple:
        :return:
        """
        run_success_msg = do_config("msg", "success_result")
        run_fail_msg = do_config("msg", "fail_result")
        new_data = Context.register_parameterization(data_namedtuple.data)
        new_url = do_config("api", "prefix_url") + data_namedtuple.url
        response = self.send_request(method=data_namedtuple.method, url=new_url, data=new_data)

        try:
            self.assertEqual(data_namedtuple.expected, response.text, msg="测试【{}】失败".format(data_namedtuple.title))
        except AssertionError as e:
            do_log.error("具体异常为：{}".format(e))
            do_excel.write_result(row=data_namedtuple.case_id+1,
                                  actual=response.text,
                                  result=run_fail_msg)
            raise e
        else:
            do_excel.write_result(row=data_namedtuple.case_id + 1,
                                  actual=response.text,
                                  result=run_success_msg)


if __name__ == '__main__':
    unittest.main()




