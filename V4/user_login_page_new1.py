"""用户登录页面业务处理"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import DriverUtil


class UserLoginObj(object):
    """获取账号框、密码框、登录按钮页面元素"""
    # 说明：对象层只获取元素对象

    def __init__(self):
        """初始化 driver 对象"""
        self.driver = DriverUtil.get_driver('user')

    # def get_element(self):
    #     """获取账号、密码、登录元素"""
    #     nameEle = self.driver.find_element(By.NAME, 'user')
    #     pwdEle = self.driver.find_element(By.NAME, 'pwd')
    #     loginEle = self.driver.find_element(By.XPATH, '//div/button[@class="btn btn-primary btn-block btn-flat"]')
    #     return [nameEle, pwdEle, loginEle]
    def get_nameEle(self):
        """获取name元素对象"""
        return self.driver.find_element(By.NAME, 'user')

    def get_pwdEle(self):
        """获取pwd元素对象"""
        return self.driver.find_element(By.NAME, 'pwd')

    def get_loginEle(self):
        """获取login元素对象"""
        return self.driver.find_element(By.XPATH, '//div/button[@class="btn btn-primary btn-block btn-flat"]')


class UserLoginHandle(object):
    """执行账号框、密码框、登录按钮操作"""
    # 说明：操作层只有操作，无逻辑执行

    def __init__(self):
        """初始化元素"""
        # self.nameEle = UserLoginObj().get_element()[0]
        # self.pwdEle = UserLoginObj().get_element()[1]
        # self.loginEle = UserLoginObj().get_element()[2]
        # self.driver = UserLoginObj().driver
        self.login_obj = UserLoginObj()

    # def exe_element(self, name, pwd):
    #     """执行输入点击清除操作"""
    #     self.nameEle.clear()
    #     self.nameEle.send_keys(name)
    #     self.pwdEle.clear()
    #     self.pwdEle.send_keys(pwd)
    #     self.loginEle.click()
    def input_name(self, name):
        """输入 name"""
        self.login_obj.get_nameEle().clear()
        self.login_obj.get_nameEle().send_keys(name)

    def input_pwd(self, pwd):
        """输入 pwd"""
        self.login_obj.get_pwdEle().clear()
        self.login_obj.get_pwdEle().send_keys(pwd)

    def click_login_btn(self):
        """点击 login 按钮"""
        self.login_obj.get_loginEle().click()

    def Pop_up_window_processing(self, expected, code):
        """错误数据对弹窗处理，正确数据判断页面标题"""
        if code == 0:  # code = 0 表示数据错误
            WebDriverWait(self.login_obj.driver, 10).until(EC.alert_is_present())
            alert = self.login_obj.driver.switch_to.alert
            assert alert.text == expected
            alert.accept()
            print(expected)
        else:  # code = 1 表示数据正确
            WebDriverWait(self.login_obj.driver, 5).until(EC.title_is(expected))

            assert self.login_obj.driver.title == expected
            print(expected)


class UserLoginTask(object):
    """将对象层与操作层结合，实现登录操作"""
    # 说明：业务层进行逻辑处理

    def __init__(self):
        """获取执行类对象"""
        self.user_login_handle = UserLoginHandle()

    def go_to_login(self, name, pwd, expected, code):
        """统一执行操作"""
        # self.userloginhandle.exe_element(name, pwd)                    # 执行输入操作
        # self.userloginhandle.Pop_up_window_processing(expected, code)  # 处理弹窗
        self.user_login_handle.input_name(name)                           # 输入账号
        self.user_login_handle.input_pwd(pwd)                             # 输入密码
        self.user_login_handle.click_login_btn()                          # 点击登录
        self.user_login_handle.Pop_up_window_processing(expected, code)   # 判断数据
