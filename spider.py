from lxml import etree
import requests
from bs4 import BeautifulSoup
from sklearn.externals import joblib
from PIL import Image
import numpy as np
model = joblib.load("svm.pkl")
# 提交表头，里面的参数是电脑各浏览器的信息。模拟成是浏览器去访问网页。
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36",
}
s = requests.session()


def predict(img):
    '''
    识别验证码
    '''
    images = []
    img = Image.open(img).convert("L")
    x_size, y_size = img.size
    y_size -= 5
    new = img.crop((4, 1, x_size - 18, y_size))
    x_size, y_size = new.size
    length = x_size // 4
    for i in range(4):
        single = new.crop((i * length, 0, (i + 1) * length, y_size))
        single = np.array(single).reshape(1, 12 * 21)
        images.append(single)
    result = ''
    for i in images:
        result += model.predict(i)[0]
    return result


def login(username, password):
    url = "http://jwc.hsu.edu.cn/default2.aspx"
    response = s.get(url)
    selector = etree.HTML(response.content)
    __VIEWSTATE = selector.xpath('//*[@id="form1"]/input/@value')[0]
    # 获取验证码并下载到本地
    imgUrl = "http://jwc.hsu.edu.cn/CheckCode.aspx?"
    imgresponse = s.get(imgUrl, stream=True)
    image = imgresponse.content
    try:
        with open("code.jpg", "wb") as f:
            f.write(image)
    except IOError:
        print("IO Error\n")
    finally:
        f.close()
    # 自动识别验证码
    code = predict('code.jpg')
    # 构建post数据
    data = {
        "__VIEWSTATE": __VIEWSTATE,
        "txtUserName": username,
        "TextBox2": password,
        "txtSecretCode": code,
        "Button1": "",
    }
    # 登陆教务系统
    response = s.post(url, data=data, headers=headers)


def getScore(username, password):
    try:
        login(username, password)
        # url是课表页面url,有个Referer参数,这个参数代表你是从哪里来的。就是登录后的主界面参数。
        url = 'http://jwc.hsu.edu.cn/xscjcx_dq.aspx?xh=%s' % username + \
            '&xm=%D0%EC%CE%B0&gnmkdm=N121621'
        headers = {
            "Referer": "http://jwc.hsu.edu.cn/xs_main.aspx?xh=%s" % username,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36",
        }
        response = s.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        # 找到form的验证参数
        __VIEWSTATE_1 = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
        data_1 = {
            '__VIEWSTATE': __VIEWSTATE_1,
            'btnCx': '查询',
        }
        response = s.post(url, data=data_1, headers=headers)
        # html代表访问页面返回的结果。
        html = response.content.decode("gb2312")
        selector = etree.HTML(html)
        course_list = []
        courses = selector.xpath('//table[2]/tr')
        head = courses[0].xpath('./td/text()')
        for course in courses[1:]:
            dic = {}
            c = course.xpath('./td/text()')
            for i in range(len(c)):
                dic[head[i]] = c[i].replace('\xa0', '')
            course_list.append(dic)
        return course_list
    except Exception as e:
        return []


if __name__ == '__main__':
    course_list = getScore('21506101058', '3.1415926')
    print(course_list)
