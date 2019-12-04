import os

# __file__固定变量
# 获取项目根目录路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CASES_DIR = os.path.join(BASE_DIR, "cases")

DATAS_DIR = os.path.join(BASE_DIR, "datas")

CONFIGS_DIR = os.path.join(BASE_DIR, "configs")

LOGS_DIR = os.path.join(BASE_DIR, "logs")

REPORTS_DIR = os.path.join(BASE_DIR, "reports")

CONFIG_FILE_PATH = os.path.join(CONFIGS_DIR, "testcase.conf")

TEST_DATAS_FILE_PATH = os.path.join(DATAS_DIR, "cases.xlsx")

USER_ACCOUNTS_FILE_PATH = os.path.join(CONFIGS_DIR, "user_accounts.conf")

