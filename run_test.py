import os
from datetime import datetime
import unittest

from libs import HTMLTestRunnerNew
from scripts.handle_config import do_config
from scripts.constants import REPORTS_DIR, USER_ACCOUNTS_FILE_PATH, CASES_DIR
from scripts.handle_user import generate_user_config

# 判断是否生成用户账号配置文件
if not os.path.exists(USER_ACCOUNTS_FILE_PATH):
    # 如果用户账号文件不存在，则创建用户账号
    generate_user_config()

one_suit = unittest.defaultTestLoader.discover(CASES_DIR)

report_html_name = os.path.join(REPORTS_DIR, do_config("report", "report_html_name"))

report_html_name_full = report_html_name + "_" + datetime.strftime(datetime.now(),"%Y%m%d%H%M%S") + ".html"

with open(report_html_name_full, mode="wb") as save_to_file:
    one_runner = HTMLTestRunnerNew.HTMLTestRunner(stream=save_to_file,
                                                  title=do_config("report","title"),
                                                  verbosity=do_config("report","verbosity"),
                                                  description=do_config("report", "description"),
                                                  tester=do_config("report","tester"))

    one_runner.run(one_suit)



