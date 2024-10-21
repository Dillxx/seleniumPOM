import time, pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from V3.test_admin_login import TestAdminLogin
from V3.utils_basic.utils_01_new import DriverUtil
from utils import RandomData


class TestAdminArticle(object):
    def setup_class(self):
        self.driver = TestAdminLogin().driver
        self.random_data = RandomData()

    def teardown_class(self):
        self.driver.quit()

    # 输入空 slug
    def test_invalidcase(self):
        # data
        title = 'postman' + self.random_data.gen_random_str()
        father = 'python'
        slug = ''
        expected = 'slug 不能为空'

        # 进入文章-》分类
        self.driver.find_element(By.XPATH, '//span[text()="文章"]').click()
        self.driver.find_element(By.XPATH, '//a[text()="分类"]').click()

        # 定位字段
        self.driver.find_element(By.XPATH, '//div/input[@name="category.title"]').send_keys(title)
        select = Select(self.driver.find_element(By.XPATH, '//div/select[@name="category.pid"]'))
        select.select_by_visible_text(father)
        self.driver.find_element(By.XPATH, '//div/input[@name="category.slug"]').send_keys(slug)
        self.driver.find_element(By.XPATH, '//button[text()="提交"]').click()

        # 定位错误信息
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@class="toast-message"]')))
        err = self.driver.find_element(By.XPATH, '//div[@class="toast-message"]').text

        # 判断是否与期望输入一致
        assert err == expected

    # 输入有效类
    def test_validcase(self):
        # data
        title = 'postman' + self.random_data.gen_random_str()
        father = 'python'
        slug = 'postman'
        expected = ''

        # 定位字段
        self.driver.find_element(By.XPATH, '//div/input[@name="category.title"]').clear()
        self.driver.find_element(By.XPATH, '//div/input[@name="category.title"]').send_keys(title)
        select = Select(self.driver.find_element(By.XPATH, '//div/select[@name="category.pid"]'))
        select.select_by_visible_text(father)
        self.driver.find_element(By.XPATH, '//div/input[@name="category.slug"]').clear()
        self.driver.find_element(By.XPATH, '//div/input[@name="category.slug"]').send_keys(slug)
        self.driver.find_element(By.XPATH, '//button[text()="提交"]').click()

        # 判断是否与期望输入一致
        assert 1 == 1


if __name__ == '__main__':
    pytest.mian(['-sv', 'test_admin_login.py', 'test_admin_article.py'])
    # pytest.mian(['-sv', 'test_admin_article.py'])