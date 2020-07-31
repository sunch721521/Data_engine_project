#A项目：爬取大众汽车的报价数据 
import requests
from bs4 import BeautifulSoup
import pandas as pd
#得到页面内容
def get_page_content(url):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    html = requests.get(url,headers=headers,timeout=10)
    content = html.text
    soup = BeautifulSoup(content,'html.parser')
    return soup

#分析页面内容
def analysis(soup):
    #找到具备报价信息的类
    info_list = soup.find_all('div',class_='search-result-list-item')
    df = pd.DataFrame(columns = ['名称', '最低价格(万元)', '最高价格(万元)', '产品图片链接'])#创建DataFrame
    for info in info_list:
        t = {}
        car_name = info.find('p',class_='cx-name text-hover').text
        img = info.find('img',class_='img')['src']#提取图片链接
        price = info.find('p',class_='cx-price').text
        #判断暂无价格的特殊情况
        if str(price) == '暂无':#判断是否暂无价格
            price_l = '暂无'#最低价格  
            price_h = '暂无'#最高价格
        else:
            #将价格分割成最低和最高两个字符串
            price_list = price.split('-',1)
            price_l = price.split('-',1)[0]
            price_h = price.split('-',1)[1][0:-1]
            
        #将各项提取内容赋值到字典中
        t['名称'], t['最低价格(万元)'], t['最高价格(万元)'], t['产品图片链接'] = \
            car_name, price_l, price_h, img
        df = df.append(t,ignore_index=True)
    return df

url = 'http://car.bitauto.com/xuanchegongju/?l=8&mid=8'#易车网大众界面网页链接
soup = get_page_content(url)#由链接获取页面内容
df = analysis(soup)#分析页面内容获取报价数据dataframe
df.to_csv('大众汽车报价.csv',index=False)#结果保存为csv文件