from configparser import ConfigParser


class HandleConfig(ConfigParser):
    """
    定义处理配置文件的类
    """
    def __init__(self):
        super().__init__()
        self.filename="testcase.conf"
        self.read(self.filename,encoding="utf-8")

    def __call__(self, section="DEFAULT", option=None,is_eval=False,is_bool=False):
        """
        对象() 这种形式，__call__方法会被调用
        :param section: 区域名
        :param option: 选项名
        :param is_eval: 是否进行eval函数转换，默认不转换
        :param is_bool: 是否需要转化为bool类型，默认不转换
        :return:
        """
        if option is None:
            return dict(self[section])

        if isinstance(is_bool,bool):
            if is_bool:
                return self.getboolean(section.option)
        else:
            raise ValueError("is_bool必须是布尔类型")

        data = self.get(section,option)

        if data.isdigit():
            return int(data)

        try:
            return float(data)
        except ValueError:
            pass

        if isinstance(is_eval,bool):
            if is_eval:
                return eval(data)
        else:
            raise ValueError("is_eval必须是布尔类型")

        return data


do_config = HandleConfig()

if __name__ == '__main__':
    config = HandleConfig()