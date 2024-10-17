import os
import pytest
import urllib3  # 忽略 urllib3 版本警告信息
import pandas as pd

from V5.user_login_page import UserLoginTask
from utils import DriverUtil, TDD

urllib3.disable_warnings()


class TestUserLogin(object):
    # 数据驱动数据
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\data" + "\\normal_user_data.csv"

    # 采用 setup_class  teardown_class 在测试用例执行之前加载驱动，执行之后关闭驱动
    def setup_class(self):
        # self.driver = DriverUtil.get_driver("user")  # 获取 driver 对象
        self.goto = UserLoginTask()

    def teardown_class(self):
        # self.driver.quit()
        DriverUtil.quit_driver()  # 退出 driver 对象

    # 错误密码
    @pytest.mark.parametrize('username, pwd, expected, code', TDD.get_user_data(path))
    def test_invaildcase(self, username, pwd, expected, code):
        """执行测试用例，包括正例反例"""
        self.goto.go_to_login(username, pwd, expected, code)  # 执行：输入数据，点击登录，处理弹窗，判断条件


if __name__ == '__main__':
    pytest.main(['-sv', __file__])
