# -*- coding: utf-8 -*-
import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib3  # 忽略 urllib3 版本警告信息

from V3.utils_basic.utils_01_new import DriverUtil
from V4.admin_login_page import AdminLoginTask
from utils import CaptchaCode, TDD

urllib3.disable_warnings()
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\data" + "\\admin_user_data.csv"


class TestAdminLogin:
    def setup_class(self):
        self.admin_login_task = AdminLoginTask()

    # def teardown_class(self):
    #     self.admin_login_task.quit_driver()

    # 正确用户名密码
    @pytest.mark.parametrize('username, pwd, captcha, expected, code', TDD.get_admin_user_data(path))
    def test_vaildcase(self, username, pwd, captcha, expected, code):
        self.admin_login_task.go_to(username, pwd, captcha, expected, code)


if __name__ == '__main__':
    pytest.mian(['-sv', __file__])
