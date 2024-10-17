"""用户登录页面业务处理"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import DriverUtil, Logger


class UserLoginObj(object):
    """获取账号框、密码框、登录按钮页面元素"""
    # 说明：对象层只获取元素对象

    def __init__(self):
        """初始化 driver 对象"""
        self.logger = Logger().get_logger()    # 日志器
        self.logger.info("用户登录测试用例开始：")
        self.driver = DriverUtil.get_driver()
        self.logger.info(f'[UserLoginObj]: 正在获取初始化driver对象:{self.driver}')

        # 说明：优化传值方式，需要修改元素值时，在初始化方法中修改即可
        #      将元素的定位方法以及特征值封装成属性，能够实现集中管理目标元素对象
        self.name = (By.NAME, 'user')   # 账号
        self.pwd = (By.NAME, 'pwd')     # 密码
        self.btn = (By.XPATH, '//div/button[@class="btn btn-primary btn-block btn-flat"]')  # 登录按钮

    def get_nameEle(self):
        """获取name元素对象"""
        self.logger.debug(f"正在定位 {self.name} 对象")
        return self.driver.find_element(*self.name)

    def get_pwdEle(self):
        """获取pwd元素对象"""
        self.logger.debug(f"正在定位 {self.pwd} 对象")
        return self.driver.find_element(*self.pwd)

    def get_loginEle(self):
        """获取login元素对象"""
        self.logger.debug(f"正在定位 {self.btn} 对象")
        return self.driver.find_element(*self.btn)


class UserLoginHandle(object):
    """执行账号框、密码框、登录按钮操作"""
    # 说明：操作层只有操作，无逻辑执行

    def __init__(self):
        """初始化元素"""
        self.login_obj = UserLoginObj()


    def input_name(self, name):
        """输入 name"""
        self.login_obj.get_nameEle().clear()
        self.login_obj.get_nameEle().send_keys(name)
        self.login_obj.logger.debug("输入用户名： %s", name)

    def input_pwd(self, pwd):
        """输入 pwd"""
        self.login_obj.get_pwdEle().clear()
        self.login_obj.get_pwdEle().send_keys(pwd)
        self.login_obj.logger.debug("输入用户密码： %s", pwd)

    def click_login_btn(self):
        """点击 login 按钮"""
        self.login_obj.get_loginEle().click()
        self.login_obj.logger.debug("点击登录按钮")

    def Pop_up_window_processing(self, expected, code):
        """错误数据对弹窗处理，正确数据判断页面标题"""
        if code == 0:  # code = 0 表示数据错误
            WebDriverWait(self.login_obj.driver, 10).until(EC.alert_is_present())
            alert = self.login_obj.driver.switch_to.alert
            try:
                assert alert.text == expected
            except AssertionError as ae1:
                self.login_obj.logger.error("=====报错了！！========= %s", ae1)
            alert.accept()
            print(f'预期结果为：{expected}')
        else:  # code = 1 表示数据正确
            WebDriverWait(self.login_obj.driver, 5).until(EC.title_is(expected))
            try:
                assert self.login_obj.driver.title == expected
            except AssertionError as ae2:
                self.login_obj.logger.error("=====报错了！！========= %s", ae2)
            print(f'预期结果为：{expected}')


class UserLoginTask(object):
    """将对象层与操作层结合，实现登录操作"""
    # 说明：业务层进行逻辑处理

    def __init__(self):
        """获取执行类对象"""
        self.user_login_handle = UserLoginHandle()

    def go_to_login(self, name, pwd, expected, code):
        """统一执行操作"""
        self.user_login_handle.input_name(name)                           # 输入账号
        self.user_login_handle.input_pwd(pwd)                             # 输入密码
        self.user_login_handle.click_login_btn()                          # 点击登录
        self.user_login_handle.Pop_up_window_processing(expected, code)   # 判断数据
        self.user_login_handle.login_obj.logger.info("用户登录测试用例结束！")
