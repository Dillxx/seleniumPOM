# -*- coding: utf-8 -*- 
# @项目：seleniumPom
# @文件：admin_article_page.py
# @作者：cndill
"""管理员页面。增加文章分类标签"""
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from V4.admin_login_page import AdminLoginPage
from V4.test_admin_login import TestAdminLogin
from utils import RandomData, DriverUtil


class ArticleAddPage(object):
    """对象层"""
    def __init__(self):
        """获取管理员登录后得 driver 对象"""
        # self.driver = TestAdminLogin().admin_login_task.admin_login_handle.admin_login_page.driver

        # self.test_admin_login = TestAdminLogin()
        # self.test_admin_login.setup_class()
        # self.driver = self.test_admin_login.admin_login_task.admin_login_handle.admin_login_page.driver

        # self.driver = AdminLoginPage().driver
        self.driver = DriverUtil.get_driver('adminUser')

        self.random_data = RandomData()
        self.essay = (By.XPATH, '//span[text()="文章"]')
        self.classify = (By.XPATH, '//a[text()="分类"]')
        self.title = (By.XPATH, '//div/input[@name="category.title"]')
        self.selector = (By.XPATH, '//div/select[@name="category.pid"]')
        self.slug = (By.XPATH, '//div/input[@name="category.slug"]')
        self.btn = (By.XPATH, '//button[text()="提交"]')
        self.message = (By.XPATH, '//div[@class="toast-message"]')

    def get_essay(self):
        """获取 essay 对象"""
        return self.driver.find_element(*self.essay)

    def get_classify(self):
        """获取 classify 对象"""
        return self.driver.find_element(*self.classify)

    def get_title(self):
        """获取 title 对象"""
        return self.driver.find_element(*self.title)

    def get_selector(self):
        """获取 selector 对象"""
        return self.driver.find_element(*self.selector)

    def get_slug(self):
        """获取 slug 对象"""
        return self.driver.find_element(*self.slug)

    def get_btn(self):
        """获取 essay 对象"""
        return self.driver.find_element(*self.btn)

    def get_message(self):
        """获取 message 对象"""
        return self.driver.find_element(*self.message)


class ArticleAddHandle(object):
    """操作层"""
    def __init__(self):
        """获取对象层对象"""
        self.article_add_page = ArticleAddPage()

    def click_essay(self):
        """点击 essay"""
        self.article_add_page.get_essay().click()

    def click_classify(self):
        """点击 classify"""
        self.article_add_page.get_classify().click()

    def click_btn(self):
        """点击 btn"""
        self.article_add_page.get_btn().click()

    def input_title(self, title):
        """输入 title 值"""
        self.article_add_page.get_title().clear()
        self.article_add_page.get_title().send_keys(title)

    def input_slug(self, slug):
        """输入 slug 值"""
        self.article_add_page.get_slug().clear()
        self.article_add_page.get_slug().send_keys(slug)

    def selector_father(self, father):
        """选择父类"""
        select = Select(self.article_add_page.get_selector())
        select.select_by_visible_text(father)

    def exe_alter(self, expected, code):
        """处理弹窗"""
        if code == '0':
            # 定位错误信息
            WebDriverWait(self.article_add_page.driver, 10).until(
                EC.visibility_of_element_located((self.article_add_page.message[0], self.article_add_page.message[1])))
            err = self.article_add_page.get_message().text
            print('------------', err, '-----------------')

            # 判断是否与期望输入一致
            assert err == expected
        elif code == '1':
            # 判断是否与期望输入一致
            assert 1 == 1


class ArticleAddTask(object):
    """业务层"""
    def __init__(self):
        """获取操作层对象"""
        self.article_Add_handle = ArticleAddHandle()

    def go_to(self, title, father, slug, expected, code):
        """执行增加分类 业务"""
        # 进入文章页面
        self.article_Add_handle.click_essay()
        # 进入分类页面
        self.article_Add_handle.click_classify()
        # 输入标题
        self.article_Add_handle.input_title(title)
        # 选择父类
        self.article_Add_handle.selector_father(father)
        # 输入slug
        if code == '0':
            slug = ''
        self.article_Add_handle.input_slug(slug)
        # 点击提交
        self.article_Add_handle.click_btn()
        # 判断
        self.article_Add_handle.exe_alter(expected, code)

    def driver_quit(self):
        """退出 driver 对象"""
        self.article_Add_handle.article_add_page.driver.quit()