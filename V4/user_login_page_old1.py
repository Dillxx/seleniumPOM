"""用户登录页面业务处理"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import DriverUtil


class UserLoginObj(object):
    """获取账号框、密码框、登录按钮页面元素"""

    def __init__(self):
        """初始化 driver 对象"""
        self.driver = DriverUtil.get_driver()

    def get_element(self):
        """获取账号、密码、登录元素"""
        nameEle = self.driver.find_element(By.NAME, 'user')
        pwdEle = self.driver.find_element(By.NAME, 'pwd')
        loginEle = self.driver.find_element(By.XPATH, '//div/button[@class="btn btn-primary btn-block btn-flat"]')
        return [nameEle, pwdEle, loginEle]


class UserLoginHandle(object):
    """执行账号框、密码框、登录按钮操作"""

    def __init__(self):
        """初始化元素"""
        self.nameEle = UserLoginObj().get_element()[0]
        self.pwdEle = UserLoginObj().get_element()[1]
        self.loginEle = UserLoginObj().get_element()[2]
        self.driver = UserLoginObj().driver

    def exe_element(self, name, pwd):
        """执行输入点击清除操作"""
        self.nameEle.clear()
        self.nameEle.send_keys(name)
        self.pwdEle.clear()
        self.pwdEle.send_keys(pwd)
        self.loginEle.click()

    def Pop_up_window_processing(self, expected, code):
        """错误数据对弹窗处理，正确数据判断页面标题"""
        if code == 0:  # code = 0 表示数据错误
            WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            assert alert.text == expected
            alert.accept()
            print(expected)
        else:  # code = 1 表示数据正确
            WebDriverWait(self.driver, 5).until(EC.title_is(expected))

            assert self.driver.title == expected
            print(expected)


class UserLoginTask(object):
    """将对象层与操作层结合，实现登录操作"""

    def __init__(self):
        """获取执行类对象"""
        self.userloginhandle = UserLoginHandle()

    def go_to_login(self, name, pwd, expected, code):
        """统一执行操作"""
        self.userloginhandle.exe_element(name, pwd)  # 执行输入操作
        self.userloginhandle.Pop_up_window_processing(expected, code)   # 处理弹窗



