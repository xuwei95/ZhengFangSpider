#-*-coding:utf-8-*-
import os
from lxml import etree
import requests
import sys
from bs4 import BeautifulSoup
import shibie

reload(sys)
# #初始参数，自己输入的学号，密码。
# studentnumber = ""
# password = ""
#访问教务系统,先得到__VIEWSTATE的值。
s = requests.session()
def login(studentnumber,password):
    url = "http://jwc.hsu.edu.cn/default2.aspx"
    response = s.get(url)
    selector = etree.HTML(response.content)
    __VIEWSTATE = selector.xpath('//*[@id="form1"]/input/@value')[0]
    #获取验证码并下载到本地
    imgUrl = "http://jwc.hsu.edu.cn/CheckCode.aspx?"
    imgresponse = s.get(imgUrl, stream=True)
    #print s.cookies
    image = imgresponse.content
    DstDir = os.getcwd()+"\\"
    #print("保存验证码到："+DstDir+"code.jpg"+"\n")
    try:
        with open(DstDir+"code.jpg" ,"wb") as jpg:
            jpg.write(image)
    except IOError:
        print("IO Error\n")
    finally:
        jpg.close
    #自动识别验证码
    code=shibie.shibie('code.jpg')
    #print '验证码识别结果为：%s'%code
    #构建post数据
    data = {
    "__VIEWSTATE":__VIEWSTATE,
    "txtUserName":studentnumber,
    "TextBox2":password,
    "txtSecretCode":code,
    "Button1":"",
    }
    #提交表头，里面的参数是电脑各浏览器的信息。模拟成是浏览器去访问网页。
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36",
    }
    #登陆教务系统
    response = s.post(url,data=data,headers=headers)
    print '登录成功'
def getScore(xh,password):
    login(xh,password)
    #url是课表页面url,有个Referer参数,这个参数代表你是从哪里来的。就是登录后的主界面参数。
    url = "http://jwc.hsu.edu.cn/xscjcx.aspx?xh=%s"%xh#&xm=%D0%EC%CE%B0&gnmkdm=N121605
    headers = {
    "Referer":"http://jwc.hsu.edu.cn/xs_main.aspx?xh=%s"%xh,
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36",
     }
    response = s.get(url,headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    # 找到form的验证参数
    __VIEWSTATE_1 = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
    name_1 = "历年成绩"
    data_1 = {
            '__VIEWSTATE':__VIEWSTATE_1,
            'btn_zcj': name_1,
        }
    response=s.post(url,data=data_1,headers=headers)
    #html代表访问页面返回的结果。
    html = response.content.decode("gb2312")
    soup = BeautifulSoup(html, 'lxml')
    table=soup.find('table', class_="datelist")
    bodytr=table.find_all('tr')
    L=[]
    for i in range(len(bodytr)):
        if i==0:
            pass
        else:
            bodytd=bodytr[i].find_all('td')
            list=[0,1,2,3,4,6,8]
            b={}
            for j in list:
                if j==0:
                    b['学年']=bodytd[j].string
                if j==1:
                    b['学期']=bodytd[j].string
                if j==2:
                    b['课程代码']=bodytd[j].string
                if j==3:
                    b['课程名称']=bodytd[j].string
                if j==4:
                    b['课程性质']=bodytd[j].string
                if j==6:
                    b['学分']=bodytd[j].string
                if j==8:
                    b['成绩']=bodytd[j].string
            L.append(b)
    return L







