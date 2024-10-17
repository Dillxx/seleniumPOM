"""公共方法提取类"""
from utils import Logger


class Base(object):
    """基础公共类"""
    def __init__(self, driver):
        """获取 webdriver 对象"""
        self.logger = Logger().get_logger()
        self.logger.info(f'[base]: 正在获取初始化driver对象:{driver}')
        self.driver = driver

    # 元素查找方法
    def find_element(self, ele_obj):
        """获取元素对象"""
        self.logger.info(f'[base]: 正在定位 {ele_obj} 对象')
        return self.driver.find_element(*ele_obj)

    # 元素输入方法
    def input_element(self, ele_obj, value):
        """对获取的元素对象输入值"""
        self.logger.info(f'[base]: 正在清空 {ele_obj} 对象')
        ele = self.find_element(ele_obj)
        ele.clear()
        # 输入日志 pass
        ele.send_keys(value)

    # 元素点击方法
    def click_element(self, ele_obj):
        """点击元素对象"""
        self.logger.info(f'[base]: 正在点击 {ele_obj} 对象')
        ele = self.find_element(ele_obj)
        ele.click()