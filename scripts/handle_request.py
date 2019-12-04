import json

import requests

from scripts.handle_log import do_log


class HttpRequest:
    """
    处理请求
    """
    def __init__(self):
        self.one_session = requests.Session()

    def __call__(self, method, url, data=None, is_json=False, **kwargs):
        method = method.lower()
        if isinstance(data,str):
            try:
                data = json.loads(data)
            except Exception as e:
                do_log.error("将json转换为Python时出现异常：{}".format(e))
                data = eval(data)

        if method == "get":
            res = self.one_session.request(method=method, url=url, data=data,**kwargs)
        elif method == "post":
            if is_json:
                res = self.one_session.request(method=method, url=url, json=data, **kwargs)
            else:
                res = self.one_session.request(method=method, url=url, data=data, **kwargs)
        else:
            res = None
            do_log.error("不支持【{}】的请求方式".format(method))

        # do_log.debug("响应信息为：{}".format(res.text))

        return res

    def close(self):
        self.one_session.close()


if __name__ == '__main__':
    login_url = 'http://test.lemonban.com:8080/futureloan/mvc/api/member/login'

    recharge_url = 'http://test.lemonban.com:8080/futureloan/mvc/api/member/recharge'

    login_params = {
        "mobilephone":"13699170001",
        "pwd":"123456"
    }

    recharge_params = {
        "mobilephone": "13699170001",
        "amount": "10000"
    }

    send_request = HttpRequest()

    send_request(method='post', url=login_url, data=login_params)

    send_request(method='post', url=recharge_url, data=recharge_params)



