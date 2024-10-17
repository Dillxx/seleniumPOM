""" 设置公共方法 """
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class DriverUtil(object):
    """存放 driver 对象"""
    driver = None  # 设置 驱动对象， 给一个初始值 ； 初始化执行一次

    def get_driver(self):
        """
        获取 driver 对象

        说明： 判断每次使用的都为同一个 driver对象
        :return: 返回 driver 对象
        """
        if self.driver is None:  # 如果是第一次创建 driver 则赋值 driver 对象
            self.options = webdriver.ChromeOptions()
            self.options.add_argument('--start-maximized')
            self.path = Service(r'F:\down_software\chrome-win\chromedriver.exe')
            self.driver = webdriver.Chrome(service=self.path, options=self.options)
            self.driver.get('http://192.168.10.130:8080/jpress/user/login')
            self.driver.implicitly_wait(10)
        return self.driver  # 如果第一次 创建driver 对象，则返回该对象；  如果是已经存在 driver对象，则跳过赋值对象，直接返回已存在的对象

    def quit_driver(self):
        """
        退出 driver 对象

        说明：保证 driver 对象存在，才能执行退出操作
        """
        if self.driver:
            self.driver.quit()
            self.driver = None  # 由于类变量在初始化类时只能赋值一次，而当前方法需要退出对象，
            # 为了在任何情况下都存在 driver 对象，因此需要再次对 driver 对象赋值


if __name__ == '__main__':
    driver = DriverUtil()
    driver.get_driver()
    driver.quit_driver()