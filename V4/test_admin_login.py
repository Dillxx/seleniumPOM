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
        # self.driverutil = DriverUtil()  # 获取 webdriver 对象
        # self.driver = self.driverutil.get_driver('adminUser')
        self.admin_login_task = AdminLoginTask()

    def teardown_class(self):
        self.admin_login_task.quit_driver()

    # 正确用户名密码
    @pytest.mark.parametrize('username, pwd, captcha, expected, code', TDD.get_admin_user_data(path))
    def test_vaildcase(self, username, pwd, captcha, expected, code):
        # self.driver.find_element(By.NAME, 'user').clear()
        # self.driver.find_element(By.NAME, 'user').send_keys(username)
        # self.driver.find_element(By.NAME, 'pwd').clear()
        # self.driver.find_element(By.NAME, 'pwd').send_keys(pwd)
        #
        # self.driver.find_element(By.NAME, 'captcha').clear()
        # if code == 1:
        #     captcha = self.driverutil.captch_code.get_VC(self.driver, '//div[@class="form-group"]/img')
        #     self.driver.find_element(By.NAME, 'captcha').send_keys(captcha)
        #     self.driver.find_element(By.XPATH, '//div/button[@class="btn btn-primary btn-block btn-flat"]').click()
        #     WebDriverWait(self.driver, 5).until(EC.title_is(expected))
        #     assert self.driver.title == expected
        # elif code == 0:
        #     self.driver.find_element(By.NAME, 'captcha').send_keys(captcha)
        #     self.driver.find_element(By.XPATH, '//div/button[@class="btn btn-primary btn-block btn-flat"]').click()
        #     WebDriverWait(self.driver, 5).until(EC.alert_is_present())
        #     alert = self.driver.switch_to.alert
        #     assert alert.text == expected
        #     alert.accept()
        self.admin_login_task.go_to(username, pwd, captcha, expected, code)


if __name__ == '__main__':
    pytest.mian(['-sv', __file__])
