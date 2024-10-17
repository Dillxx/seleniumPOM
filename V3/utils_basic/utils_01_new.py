""" 设置公共方法 """
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class DriverUtil(object):
    """存放 __driver 对象"""
    # 说明：将 driver 对象 设置为 私有对象 __driver 防止外界访问修改
    # 方法：使用 ctrl+r 批量替换
    __driver = None  # 设置 驱动对象， 给一个初始值 ； 初始化执行一次

    @classmethod
    def get_driver(cls):
        """
        获取 __driver 对象

        说明： 判断每次使用的都为同一个 driver对象
        :return: 返回 driver 对象
        """
        if cls.__driver is None:  # 如果是第一次创建 __driver 则赋值 __driver 对象
            cls.option = webdriver.ChromeOptions()
            cls.option.add_argument('--start-maximized')
            cls.path = Service(r'F:\down_software\chrome-win\chromedriver.exe')
            cls.__driver = webdriver.Chrome(service=cls.path, options=cls.option)
            cls.__driver.get('http://192.168.10.130:8080/jpress/user/login')
            cls.__driver.implicitly_wait(10)
        return cls.__driver  # 如果第一次 创建__driver 对象，则返回该对象；  如果是已经存在 __driver对象，则跳过赋值对象，直接返回已存在的对象

    @classmethod
    def quit_driver(cls):
        """
        退出 driver 对象

        说明：保证 driver 对象存在，才能执行退出操作
        """
        if cls.__driver:
            cls.__driver.quit()
            cls.__driver = None  # 由于类变量在初始化类时只能赋值一次，而当前方法需要退出对象，
            # 为了在任何情况下都存在 __driver 对象，因此需要再次对 __driver 对象赋值


if __name__ == '__main__':
    # 说明： 实例方法 替换为 类方法，省略实例化类步骤

    DriverUtil.get_driver()
    DriverUtil.quit_driver()