from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from untl.util import gen_random_str


class TestAdminArticleCtr:
    def __init__(self, login):
        self.login = login

    # 发布文章
    def test_addArtivle(self):
        # 数据
        title = f'测试{gen_random_str()}'
        content = f'这是{title}的内容'
        expected = '文章保存成功。'


        # 进入写文章页面
        self.login.driver.find_element(By.XPATH, '//span[text()="文章"]').click()
        self.login.driver.find_element(By.XPATH, '//a[text()="写文章"]').click()

        # 定位元素输入数据
        self.login.driver.find_element(By.ID, 'article-title').send_keys(title)
        # 切换到iframe
        self.login.driver.switch_to.frame(0)
        self.login.driver.find_element(By.XPATH, '//body[@class="cke_editable cke_editable_themed cke_contents_ltr cke_show_borders"]').send_keys(content)
        # 退出当前iframe
        self.login.driver.switch_to.default_content()

        # 点击发布
        self.login.driver.find_element(By.XPATH, '//button[@data-status="normal"]').click()

        # 捕获弹窗提示信息
        WebDriverWait(self.login.driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@class="toast-message"]')))
        content = self.login.driver.find_element(By.XPATH, '//div[@class="toast-message"]').text

        # 判断结果是否与预期一致
        assert content == expected

    # 删除单个文章
    def test_deleteOneArtical(self):
        # 进入文章管理页面
        self.login.driver.find_element(By.XPATH, '//span[text()="文章"]').click()
        self.login.driver.find_element(By.XPATH, '//a[text()="文章管理"]').click()

        # 获取文章数量
        pre_numbers = len(self.login.driver.find_elements(By.XPATH, '//tr[@class="jp-actiontr"]'))

        # 删除文章
        hover = self.login.driver.find_element(By.XPATH, '//strong/a[1]')
        ActionChains(self.login.driver).move_to_element(hover).perform()
        self.login.driver.find_element(By.XPATH, '//a[text()="垃圾箱"]').click()

        # 获取删除后的文章数量
        aft_numbers = len(self.login.driver.find_elements(By.XPATH, '//tr[@class="jp-actiontr"]'))

        # 判断前后文章数量
        assert aft_numbers == (pre_numbers - 1)
        print(f'pre{pre_numbers}, aft{aft_numbers}')

    # 删除全部文章
    def test_deleteAllArtical(self):
        # 进入文章管理页面
        self.login.driver.find_element(By.XPATH, '//span[text()="文章"]').click()
        self.login.driver.find_element(By.XPATH, '//a[text()="文章管理"]').click()

        # 获取文章数量
        pre_numbers = len(self.login.driver.find_elements(By.XPATH, '//tr[@class="jp-actiontr"]'))

        # 删除文章
        self.login.driver.find_element(By.XPATH, '//input[@name="dataItem"]').click()
        self.login.driver.find_element(By.XPATH, '//button[text()=" 批量删除"]').click()
        WebDriverWait(self.login.driver, 5).until(EC.alert_is_present())
        alert = self.login.driver.switch_to.alert
        alert.accept()

        # 获取删除后的文章数量
        # 等到文章元素不存在后 再统计数量
        WebDriverWait(self.login.driver, 5).until(EC.invisibility_of_element_located((By.XPATH, '//tr[@class="jp-actiontr"]')))
        aft_numbers = len(self.login.driver.find_elements(By.XPATH, '//tr[@class="jp-actiontr"]'))

        # 判断前后文章数量
        print(f'pre{pre_numbers}, aft{aft_numbers}')
        assert aft_numbers == 0


