import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib3  # 忽略 urllib3 版本警告信息
from utils import CaptchaCode, TDD

urllib3.disable_warnings()
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\data" + "\\admin_user_data.csv"




class TestAdminLogin:
    def setup_class(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--start-maximized')
        self.path = Service(r'F:\down_software\chrome-win\chromedriver.exe')
        self.driver = webdriver.Chrome(service=self.path, options=self.options)
        self.driver.get('http://192.168.10.130:8080/jpress/admin/login')
        self.driver.implicitly_wait(10)
        self.captch_code = CaptchaCode()   # 实例化验证码处理对象

    def teardown_class(self):
        self.driver.quit()

    # def __init__(self):
    #     self.options = webdriver.ChromeOptions()
    #     self.options.add_argument('--start-maximized')
    #     self.path = Service(r'F:\down_software\chrome-win\chromedriver.exe')
    #     self.driver = webdriver.Chrome(service=self.path, options=self.options)
    #     self.driver.get('http://192.168.10.130:8080/jpress/admin/login')
    #     self.driver.implicitly_wait(10)

    # 空验证码
    # @pytest.mark.parametrize('username, pwd, captcha, expected, code', TDD.get_admin_user_data(path))
    # def test_invaildcase(self):
    #     username = 'admin'
    #     pwd = 'admin123'
    #     captcha = ''
    #     expected = '验证码不能为空'
    #
    #     self.driver.find_element(By.NAME, 'user').send_keys(username)
    #     self.driver.find_element(By.NAME, 'pwd').send_keys(pwd)
    #     self.driver.find_element(By.NAME, 'captcha').send_keys(captcha)
    #     self.driver.find_element(By.XPATH, '//div/button[@class="btn btn-primary btn-block btn-flat"]').click()
    #
    #     WebDriverWait(self.driver, 5).until(EC.alert_is_present())
    #     alert = self.driver.switch_to.alert
    #
    #     assert alert.text == expected
    #     alert.accept()

    # 正确用户名密码
    @pytest.mark.parametrize('username, pwd, captcha, expected, code', TDD.get_admin_user_data(path))
    def test_vaildcase(self, username, pwd, captcha, expected, code):
        # username = 'admin'
        # pwd = 'admin123'
        # captcha = ''
        # expected = 'JPress后台'

        self.driver.find_element(By.NAME, 'user').clear()
        self.driver.find_element(By.NAME, 'user').send_keys(username)
        self.driver.find_element(By.NAME, 'pwd').clear()
        self.driver.find_element(By.NAME, 'pwd').send_keys(pwd)

        self.driver.find_element(By.NAME, 'captcha').clear()
        if code == 1:
            captcha = self.captch_code.get_VC(self.driver, '//div[@class="form-group"]/img')
            self.driver.find_element(By.NAME, 'captcha').send_keys(captcha)
            self.driver.find_element(By.XPATH, '//div/button[@class="btn btn-primary btn-block btn-flat"]').click()
            WebDriverWait(self.driver, 5).until(EC.title_is(expected))
            assert self.driver.title == expected
        elif code == 0:
            self.driver.find_element(By.NAME, 'captcha').send_keys(captcha)
            self.driver.find_element(By.XPATH, '//div/button[@class="btn btn-primary btn-block btn-flat"]').click()
            WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            assert alert.text == expected
            alert.accept()



if __name__ == '__main__':
    pytest.mian(['-sv', 'test_admin_login.py'])