from scripts.handle_mysql import HandleMysql
from scripts.handle_request import HttpRequest
from scripts.handle_config import do_config
from scripts.constants import USER_ACCOUNTS_FILE_PATH

def create_new_user(regname, pwd="123456"):
    """
    创建一个新用户
    :return:
    """
    handle_mysql = HandleMysql()
    send_request = HttpRequest()
    url = do_config("api", "prefix_url")+"/member/register"
    sql = "select 'Id' from future.`member` where `MobilePhone`=%s;"
    while True:
        mobilephone = handle_mysql.create_not_existed_mobile()
        data = {"mobilephone":mobilephone,"pwd":pwd,"regname":regname}
        send_request(method="post", url=url, data=data)
        result = handle_mysql(sql=sql, arg=(mobilephone,))
        if result:
            user_id = result["Id"]
            break

    user_dict = {
        regname:{
            "Id":user_id,
            "regname":regname,
            "mobilephone":mobilephone,
            "pwd":pwd
        }
    }
    handle_mysql.close()
    send_request.close()
    return user_dict

def generate_user_config():
    """
    生成三个用户信息
    :return:
    """
    user_data_dict = {}
    user_data_dict.update(create_new_user("admin_user"))
    user_data_dict.update(create_new_user("invest_user"))
    user_data_dict.update(create_new_user("borrow_user"))
    do_config.write_config(user_data_dict,USER_ACCOUNTS_FILE_PATH)

if __name__ == '__main__':
    generate_user_config()

