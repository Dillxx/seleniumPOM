import os

from V0.test_user_login import TestUserLogin

if __name__ == '__main__':
    # pytest.main(['-sv', __file__])
    # userLogin = TestUserLogin()
    # userLogin.test_invaildcase()
    # userLogin.test_wrong_account()
    # userLogin.test_vaildcase()
    import pandas as pd
    #
    #
    # def get_data():
    #     data = pd.read_csv(r'D:\桌面\测试开发\Postman\seleniumPom\data\pytestDemo.csv', encoding='GB2312')
    #     data1 = []
    #     for i in range(len(data['username'])):
    #         data1.append((data['username'][i], str(data['pwd'][i]), data['expected'][i]))
    #     return data1
    # print(get_data())

    # import chardet
    #
    # with open('D:\桌面\测试开发\Postman\seleniumPom\data\data.csv', 'rb') as f:
    #     result = chardet.detect(f.read())  # 读取一定量的数据进行编码检测
    #
    # print(result['encoding'])  # 打印检测到的编码

    # def get_excel_data():
    #     data = pd.read_excel(r'D:\桌面\测试开发\Postman\seleniumPom\data\data.xlsx', sheet_name=0)
    #     data1 = []
    #     for i in range(len(data['username'])):
    #         data1.append([data['username'][i], str(data['pwd'][i]), data['expected'][i]])
    #         # print(type(data['pwd'][i]), type(str(data['pwd'][i])), str(data['pwd'][i]))
    #     print(data1)
    #     return data
    #
    #
    # print(get_excel_data())

    # def add(*args):
    #     a, b = args
    #     return a+b
    #
    #
    # print(add(1, 3))
