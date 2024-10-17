""" 设置公共方法 """
import datetime
import logging
import os
import random
import time
import logging.handlers
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
from PIL import Image
from selenium.webdriver.common.by import By

from chaojiying_Python.chaojiying import Chaojiying_Client


class DriverUtil(object):
    """存放 __driver 对象"""
    # 说明：将 driver 对象 设置为 私有对象 __driver 防止外界访问修改
    # 方法：使用 ctrl+r 批量替换
    __driver = None  # 设置 驱动对象， 给一个初始值 ； 初始化执行一次

    @classmethod
    def get_driver(cls, Name_code):
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
            if Name_code == 'user':
                cls.__driver.get('http://192.168.10.130:8080/jpress/user/login')
            elif Name_code == 'adminUser':
                cls.__driver.get('http://192.168.10.130:8080/jpress/admin/login')
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





class TDD(object):
    """数据驱动 获取 csv 设定值"""

    @classmethod
    def get_user_data(cls, path):
        """
        用户登录--账号-密码-预期值
        :return:
        """
        # path = os.path.dirname(os.path.abspath(__file__)) + "\\data" + "\\normal_user_data.csv"
        data = pd.read_csv(path, encoding='GB2312')
        data1 = []
        for i in range(len(data['username'])):
            data1.append((data['username'][i], str(data['pwd'][i]), data['expected'][i], data['code'][i]))
        return data1

    @classmethod
    def get_admin_user_data(cls, path):
        """
        用户登录--账号-密码-预期值
        :return:
        """
        # path = os.path.dirname(os.path.abspath(__file__)) + "\\data" + "\\normal_user_data.csv"
        data = pd.read_csv(path, encoding='GB2312')
        data1 = []
        for i in range(len(data['username'])):
            data1.append((data['username'][i], str(data['pwd'][i]), str(data['captcha'][i]), data['expected'][i], data['code'][i]))
        return data1



class Logger(object):
    """日志器"""
    logger = None

    @classmethod
    def get_logger(cls):
        """获取日志提取器"""

        if cls.logger == None:
            # 初始化日志器
            cls.logger = logging.getLogger('mylogger')  # 设置日志器名称
            cls.logger.setLevel(logging.DEBUG)  # 设置日志等级为 debug，将获取所有 日志等级信息

            # 设置旋转日志处理器（TimedRotatingFileHandler（日志名称，轮转时间， 指定轮转天数， 备份数量， 轮转时间特定时间点））
            """
            参数：
                when: 指定滚动的时间单位，例如 'S'（秒）、'M'（分钟）、'H'（小时）、'D'（天）、'midnight'（每天午夜）。
                interval: 结合 when 使用，指定触发滚动的时间间隔。例如，interval=1 和 when='D' 代表每天滚动一次。
                backupCount: 保留的备份文件数量。超过这个数量时，旧的日志文件会被删除。
                atTime: 指定一天中的具体时间点进行日志切换。
            """
            rf_handler = logging.handlers.TimedRotatingFileHandler(
                os.path.dirname(os.path.abspath(__file__)) + '\\V6\\logs\\all.log', when='midnight', interval=1,
                backupCount=7,
                atTime=datetime.time(0, 0, 0,
                                     0))  # 创建一个旋转日志处理器，名称为 al.log，每天午夜12点整自动轮转，备份7个日志
            rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))  # 设置日志输出格式

            # 设置日志错误处理器（FileHandler）
            f_handler = logging.FileHandler(
                os.path.dirname(os.path.abspath(__file__)) + '\\V6\\logs\\error.log')  # 设置日志错误文件名
            f_handler.setLevel(logging.ERROR)  # 设置日志等级
            f_handler.setFormatter(
                logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))  # 设置日志输出格式

            # 将日志处理器添加到日志器中
            cls.logger.addHandler(rf_handler)
            cls.logger.addHandler(f_handler)
        return cls.logger


class CaptchaCode(object):
    """处理验证码"""

    def get_VC(self, driver, pic_id):
        """
        # 获取验证码图片
        :param driver: chrome webdriver
        :param pic_id: 验证码定位元素
        :return: 验证码图片字符串
        """
        # driver.implicitly_wait(10)
        # 截取全屏
        time1 = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
        img_path = os.path.dirname(os.path.abspath(__file__)) + '\\' + 'screenshots' + '\\' + time1 + '.png'
        # print(img_path)
        driver.save_screenshot(img_path)

        # 获取验证码元素定位
        img_ele = driver.find_element(By.XPATH, pic_id)
        # 获取验证码图片在屏幕中的位置
        loca = img_ele.location
        size = img_ele.size
        # 获取屏幕是缩放比
        dpr = driver.execute_script('return window.devicePixelRatio')

        # 由于 当前屏幕缩放率为 125% ，会影响原来的 100% 缩放比，导致截取不到验证码图片，因此 *1.25 解决该问题
        # rangle = (loca['x'] * 1.25, loca['y'] * 1.25, size['width'] * 1.25 + loca['x'] * 1.25,
        #           size['height'] * 1.25 + loca['y'] * 1.25)
        rangle = (loca['x'] * dpr, loca['y'] * dpr, size['width'] * dpr + loca['x'] * dpr,
                  size['height'] * dpr + loca['y'] * dpr)

        # 打开上面保存的全屏截图图片
        i = Image.open(img_path)
        # 截取并保存验证码图片， crop 传入元组参数：左-上-右-下
        img_yanzheng = i.crop(rangle)
        time2 = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time())) + str(random.randint(1, 1000))
        img_path2 = os.path.dirname(os.path.abspath(__file__)) + '\\' + 'screenshots' + '\\' + time1 + '.png'
        img_yanzheng.save(img_path2)
        pic_str = self.get_yanzheng(img_path2)
        return pic_str

    def get_yanzheng(self, img):
        """
        # 超级鹰识别验证码
        :param img: 验证码图片
        :return: 验证码字符串
        """
        chaojiying = Chaojiying_Client('cndill', '123456789Qx.', '963468')  # 用户中心>>软件ID 生成一个替换 96001
        im = open(img, 'rb').read()  # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
        pic_str = chaojiying.PostPic(im, 1004)['pic_str']
        return pic_str


# if __name__ == '__main__':
# 说明： 实例方法 替换为 类方法，省略实例化类步骤
#
# DriverUtil.get_driver()
# DriverUtil.quit_driver()
#     path = os.path.dirname(os.path.abspath(__file__)) + "\\data" + "\\admin_user_data.csv"
#     print(TDD.get_admin_user_data(path))
#     a = 'nan'
#     a = '2434'
#     print(a)
# print(os.path.dirname(os.path.abspath(__file__)) + '\\V6\\logs\\all.log')
