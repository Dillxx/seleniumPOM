import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib3  # 忽略 urllib3 版本警告信息
import pandas as pd

from V4.user_login_page_old1 import UserLoginTask
from utils import DriverUtil, TDD

urllib3.disable_warnings()


class TestUserLogin(object):
    # 数据驱动数据
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\data" + "\\pytestDemo.csv"

    # 采用 setup_class  teardown_class 在测试用例执行之前加载驱动，执行之后关闭驱动
    def setup_class(self):
        self.driver = DriverUtil.get_driver()  # 获取 driver 对象
        self.goto = UserLoginTask()

    def teardown_class(self):
        # self.driver.quit()
        DriverUtil.quit_driver()  # 退出 driver 对象

    # 错误密码
    @pytest.mark.parametrize('username, pwd, expected, code', TDD.get_user_data(path))
    def test_invaildcase(self, username, pwd, expected, code):
        # self.driver.find_element(By.NAME, 'user').clear()
        # self.driver.find_element(By.NAME, 'user').send_keys(username)
        # self.driver.find_element(By.NAME, 'pwd').clear()
        # self.driver.find_element(By.NAME, 'pwd').send_keys(pwd)
        # self.driver.find_element(By.XPATH, '//div/button[@class="btn btn-primary btn-block btn-flat"]').click()
        # WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        # alert = self.driver.switch_to.alert
        #
        # assert alert.text == expected
        # alert.accept()
        self.goto.go_to_login(username, pwd, expected, code)  # 执行：输入数据，点击登录，处理弹窗，判断条件

    # 正确用户名密码
    # @pytest.mark.parametrize('username, pwd, expected', [('admin', 'admin123', '用户中心')])
    # def test_vaildcase(self, username, pwd, expected):
    #
    #     self.driver.find_element(By.NAME, 'user').clear()
    #     self.driver.find_element(By.NAME, 'user').send_keys(username)
    #     self.driver.find_element(By.NAME, 'pwd').clear()
    #     self.driver.find_element(By.NAME, 'pwd').send_keys(pwd)
    #     self.driver.find_element(By.XPATH, '//div/button[@class="btn btn-primary btn-block btn-flat"]').click()
    #
    #     WebDriverWait(self.driver, 5).until(EC.title_is(expected))
    #
    #     assert self.driver.title == expected


if __name__ == '__main__':
    pytest.main(['-sv', __file__])
