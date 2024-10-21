# -*- coding: utf-8 -*-
"""管理员登录页面"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import DriverUtil, CaptchaCode


class AdminLoginPage(object):
    """管理员登录对象层"""

    def __init__(self):
        """获取 webdriver 对象"""
        self.driver_util = DriverUtil()  # 实例化 webdriver对象
        self.driver = self.driver_util.get_driver('adminUser')

    def get_username(self):
        """获取 username 元素对象"""
        return self.driver.find_element(By.NAME, 'user')

    def get_pwd(self):
        """获取 pwd 元素对象"""
        return self.driver.find_element(By.NAME, 'pwd')

    def get_captcha(self):
        """获取 captcha 元素对象"""
        return self.driver.find_element(By.NAME, 'captcha')

    def get_btn(self):
        """获取 btn 元素对象"""
        return self.driver.find_element(By.XPATH, '//div/button[@class="btn btn-primary btn-block btn-flat"]')


class AdminLoginHandle(object):
    """管理员登录操作层"""

    def __init__(self):
        """获取对象层元素对象"""
        self.admin_login_page = AdminLoginPage()
        self.captcha_code = CaptchaCode()

    def input_username(self, username):
        """输入 username 值"""
        self.admin_login_page.get_username().clear()
        self.admin_login_page.get_username().send_keys(username)

    def input_pwd(self, pwd):
        """输入 pwd 值"""
        self.admin_login_page.get_pwd().clear()
        self.admin_login_page.get_pwd().send_keys(pwd)

    def input_captcha(self, captcha):
        """输入 captcha 值"""
        self.admin_login_page.get_captcha().clear()
        self.admin_login_page.get_captcha().send_keys(captcha)

    def click_btn(self):
        """点击 btn 登录按钮"""
        self.admin_login_page.get_btn().click()

    def assignment_alert(self, expected, code):
        """弹窗处理"""
        if code == '0':
            WebDriverWait(self.admin_login_page.driver, 5).until(EC.alert_is_present())
            alert = self.admin_login_page.driver.switch_to.alert
            assert alert.text == expected
            alert.accept()
        elif code == '1':
            # captcha = self.captcha_code.get_VC(self.admin_login_page.driver, '//div[@class="form-group"]/img')
            WebDriverWait(self.admin_login_page.driver, 5).until(EC.title_is(expected))
            assert self.admin_login_page.driver.title == expected

    def get_captcha_value(self):
        """获取验证码图片中的值"""
        return self.captcha_code.get_VC(self.admin_login_page.driver, '//div[@class="form-group"]/img')


class AdminLoginTask(object):
    """管理员登录业务层"""

    def __init__(self):
        """获取操作层对象"""
        self.admin_login_handle = AdminLoginHandle()

    def quit_driver(self):
        """退出 driver"""
        self.admin_login_handle.admin_login_page.driver_util.quit_driver()

    def go_to(self, username, pwd, captcha, expected, code):
        """管理员登录业务流程"""
        # 输入账号
        self.admin_login_handle.input_username(username)
        # 输入密码
        self.admin_login_handle.input_pwd(pwd)
        # 输入验证码
        if code == '1':
            captcha = self.admin_login_handle.get_captcha_value()
        self.admin_login_handle.input_captcha(captcha)
        # 点击登录
        self.admin_login_handle.click_btn()
        # 判断弹窗
        self.admin_login_handle.assignment_alert(expected, code)
