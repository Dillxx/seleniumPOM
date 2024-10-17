import os
import pickle
import random
import string
import time
import datetime
import logging
import logging.handlers
from PIL import Image
from selenium.webdriver.common.by import By

from chaojiying_Python.chaojiying import Chaojiying_Client


def get_VC(driver, pic_id):
    """
    # 获取验证码图片内容
    :param driver: chrome webdriver
    :param pic_id: 验证码定位元素
    :return: 验证码图片字符串
    """
    # driver.implicitly_wait(10)
    # 截取全屏
    time1 = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
    img_path = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))) + '\\' + 'screenshots' + '\\' + time1 + '.png'
    print(img_path)
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
    img_path2 = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))) + '\\' + 'screenshots' + '\\' + time1 + '.png'
    img_yanzheng.save(img_path2)
    pic_str = get_yanzheng(img_path2)
    return pic_str


def get_yanzheng(img):
    """
    # 超级鹰识别验证码
    :param img: 验证码图片
    :return: 验证码字符串
    """
    chaojiying = Chaojiying_Client('cndill', '123456789Qx.', '963468')  # 用户中心>>软件ID 生成一个替换 96001
    im = open(img, 'rb').read()  # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
    pic_str = chaojiying.PostPic(im, 1004)['pic_str']
    return pic_str


def gen_random_str():
    """
    # 生成一个 8位 的随机字符串（字母+数字）
    :return:
    """
    rand_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    return rand_str


def save_cookie(driver, path):
    """
    # 保存 cookies
    :param driver: chrome webdriver
    :param path:
    :return:
    """
    with open(path, 'wb') as f:
        cookies = driver.get_cookies()
        pickle.dump(cookies, f)


def load_cookie(driver, path):
    """
    # 添加 cookies 信息
    :param driver:
    :param path:
    :return:
    """
    with open(path, 'rb') as f:
        cookies = pickle.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)


def get_logger():
    # 初始化日志器
    logger = logging.getLogger('mylogger')  # 设置日志器名称
    logger.setLevel(logging.DEBUG)  # 设置日志等级为 debug，将获取所有 日志等级信息

    # 设置旋转日志处理器（TimedRotatingFileHandler（日志名称，轮转时间， 指定轮转天数， 备份数量， 轮转时间特定时间点））
    """
    参数：
        when: 指定滚动的时间单位，例如 'S'（秒）、'M'（分钟）、'H'（小时）、'D'（天）、'midnight'（每天午夜）。
        interval: 结合 when 使用，指定触发滚动的时间间隔。例如，interval=1 和 when='D' 代表每天滚动一次。
        backupCount: 保留的备份文件数量。超过这个数量时，旧的日志文件会被删除。
        atTime: 指定一天中的具体时间点进行日志切换。
    """
    rf_handler = logging.handlers.TimedRotatingFileHandler('all.log', when='midnight', interval=1, backupCount=7,
                                                           atTime=datetime.time(0, 0, 0,
                                                                                0))  # 创建一个旋转日志处理器，名称为 al.log，每天午夜12点整自动轮转，备份7个日志
    rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))  # 设置日志输出格式

    # 设置日志错误处理器（FileHandler）
    f_handler = logging.FileHandler('error.log')  # 设置日志错误文件名
    f_handler.setLevel(logging.ERROR)  # 设置日志等级
    f_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))  # 设置日志输出格式

    # 将日志处理器添加到日志器中
    logger.addHandler(rf_handler)
    logger.addHandler(f_handler)
    return logger

