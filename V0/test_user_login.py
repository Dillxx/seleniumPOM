import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib3  # 忽略 urllib3 版本警告信息

urllib3.disable_warnings()


# 由于 pytest 不允许类中存在 初始化函数 __init__，因此第一想法是通过夹具设置范围为 class， 但由于每次执行测试用例都需要重新驱动浏览器、关闭浏览器，弃用
# @pytest.fixture(scope='class')
# def exe():
#     options = webdriver.ChromeOptions()
#     options.add_argument('--start-maximized')
#     path = Service(r'F:\down_software\chrome-win\chromedriver.exe')
#     driver = webdriver.Chrome(service=path, options=options)
#     driver.get('http://192.168.10.130:8080/jpress/user/login')
#     driver.implicitly_wait(10)
#     yield
#     driver.quit()

class TestUserLogin(object):
    # 采用 setup_class  teardown_class 在测试用例执行之前加载驱动，执行之后关闭驱动
    def setup_class(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--start-maximized')
        self.path = Service(r'F:\down_software\chrome-win\chromedriver.exe')
        self.driver = webdriver.Chrome(service=self.path, options=self.options)
        self.driver.get('http://192.168.10.130:8080/jpress/user/login')
        self.driver.implicitly_wait(10)

    def teardown_class(self):
        self.driver.quit()

    # def __init__(self):
    #     self.options = webdriver.ChromeOptions()
    #     self.options.add_argument('--start-maximized')
    #     self.path = Service(r'F:\down_software\chrome-win\chromedriver.exe')
    #     self.driver = webdriver.Chrome(service=self.path, options=self.options)
    #     self.driver.get('http://192.168.10.130:8080/jpress/user/login')
    #     self.driver.implicitly_wait(10)

    # 错误密码
    def test_invaildcase(self):
        username = 'admin'
        pwd = '123456'
        expected = '用户名或密码不正确'

        self.driver.find_element(By.NAME, 'user').send_keys(username)
        self.driver.find_element(By.NAME, 'pwd').send_keys(pwd)
        self.driver.find_element(By.XPATH, '//div/button[@class="btn btn-primary btn-block btn-flat"]').click()

        WebDriverWait(self.driver, 5).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert

        assert alert.text == expected
        alert.accept()

    # 错误账号
    def test_wrong_account(self):
        username = 'admin123'
        pwd = '123456'
        expected = '用户名不正确。'

        self.driver.find_element(By.NAME, 'user').clear()
        self.driver.find_element(By.NAME, 'user').send_keys(username)
        self.driver.find_element(By.NAME, 'pwd').clear()
        self.driver.find_element(By.NAME, 'pwd').send_keys(pwd)
        self.driver.find_element(By.XPATH, '//div/button[@class="btn btn-primary btn-block btn-flat"]').click()

        WebDriverWait(self.driver, 5).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert

        assert expected == alert.text
        alert.accept()

    # 正确用户名密码
    def test_vaildcase(self):
        username = 'admin'
        pwd = 'admin123'
        expected = '用户中心'

        self.driver.find_element(By.NAME, 'user').clear()
        self.driver.find_element(By.NAME, 'user').send_keys(username)
        self.driver.find_element(By.NAME, 'pwd').clear()
        self.driver.find_element(By.NAME, 'pwd').send_keys(pwd)
        self.driver.find_element(By.XPATH, '//div/button[@class="btn btn-primary btn-block btn-flat"]').click()

        WebDriverWait(self.driver, 5).until(EC.title_is(expected))

        assert self.driver.title == expected


if __name__ == '__main__':
    pytest.main(['-sv', __file__])
