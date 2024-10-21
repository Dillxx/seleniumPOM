# -*- coding: utf-8 -*-
import os
import pytest
import urllib3  # 忽略 urllib3 版本警告信息
from V5.admin_login_page import AdminLoginTask
from utils import TDD
urllib3.disable_warnings()


class TestAdminLogin:
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\data" + "\\admin_user_data.csv"

    def setup_class(self):
        self.admin_login_task = AdminLoginTask()

    def teardown_class(self):
        self.admin_login_task.quit_driver()

    # 正确用户名密码
    @pytest.mark.parametrize('username, pwd, captcha, expected, code', TDD.get_admin_user_data(path))
    def test_vaildcase(self, username, pwd, captcha, expected, code):
        self.admin_login_task.go_to(username, pwd, captcha, expected, code)


if __name__ == '__main__':
    pytest.mian(['-sv', __file__])
