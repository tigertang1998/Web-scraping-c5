# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 23:25:25 2018

@author: TIGER

发历史数据，历史均价
"""


#https://www.c5game.com/dota/20958-S.html

import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString ## cookies 加工
import time
import random
import smtplib
from email.mime.text import MIMEText
import re

def get_history_url(item_id):
    item_id_str = str(item_id)
    url = 'https://www.c5game.com/dota/history/' + item_id_str + '.html'  #爬历史数据
    return url

def get_selling_prices_url(item_id):
    item_id_str = str(item_id)
    url = 'https://www.c5game.com/dota/' + item_id_str + '-S.html'  #爬售出数据
    return url


def get_html(url):
    r = requests.get(url)
    r.encoding='utf-8'
    return r.text




def get_history_prices(item_id):
    contents = []
    url = get_history_url(item_id)
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    ###常规操作，做汤
    sales = soup.find_all('tr')    
    for sale in sales[1:12]:   #######！！！重要，因为第一个是没有值的，导致text.strip()出错了
        content = {}
        try:
            content['时间'] = sale.find('td', attrs = {'style' : 'padding:10px 30px;'}).text.strip()
            content['价格'] = sale.find('span', attrs = {'class' : 'ft-gold'}).text.strip()
            contents.append(content)
            #if content not in contents:   需要去重版本
                #contents.append(content)
        except:
            print('wrong')
    ####找到十条交易记录并加到contents中

    
    sum = 0
    for i in range(len(contents)):###因为第0项是名字
        sum = sum + float((re.findall('\d\d\.?\d',list(contents[i].values())[1]))[0])
    avg_history_prices = sum/len(contents)
    contents.append({'avg_hisotry_prices':avg_history_prices})
    ####算均值
    return contents



def get_agent():
    agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'AppleWebKit/537.36 (KHTML, like Gecko)', 'Chrome/68.0.3440.106', 'Safari/537.36']
    random_agent = agents[random.randint(0,len(agents))]
    agent_dict = {'User_agent':random_agent}
    return agent_dict
    
raw_cookies = 'C5Appid=730; C5NoticeBounces1535708411=close; C5NoticeBounces1535724406=close; C5Machines=vLFi2iMraVoSe%2F8OOrw3iQ%3D%3D; C5SessionID=2lcg3j3t3q1ve0uvqvtg2kdf66; C5Sate=0de8b78c4925e35303ef93bafdcb1acc548b8baaa%3A4%3A%7Bi%3A0%3Bs%3A9%3A%22557556557%22%3Bi%3A1%3Bs%3A11%3A%22q1070880522%22%3Bi%3A2%3Bi%3A259200%3Bi%3A3%3Ba%3A0%3A%7B%7D%7D; C5Token=5b8b7096127ec; C5Login=557556557; C5_NPWD=vLFi2iMraVoSe%2F8OOrw3iQ%3D%3D; buyKnowNotice=close; Hm_lvt_86084b1bece3626cd94deede7ecf31a8=1535727195,1535727880,1535864870,1535870551; Hm_lpvt_86084b1bece3626cd94deede7ecf31a8=1535870777; C5Lang=zh'




def get_cookies():
    cookies = {}
    for line in raw_cookies.split(';'):
        key, value = line.split('=', 1)
        cookies[key]  = value  ##需要 dic形式的cookies
    return cookies



headers = {'User_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
          'Cookie': raw_cookies
          }
    


def get_html_get_selling_prices(url):
    r = requests.get(url, headers = headers)
    r.encoding='utf-8'
    return r.text
#Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36



def get_selling_prices(item_id):
    url = get_selling_prices_url(item_id)
    html = get_html_get_selling_prices(url)
    soup = BeautifulSoup(html, 'lxml')
    sales = soup.find_all('tr')    
    for sale in sales[2:12]:   #######！！！重要，因为第一个是没有值的，导致text.strip()出错了
        content = {}##########需要修改， c5 可能有反爬虫
        try:
            content['时间'] = sale.find('td', attrs = {'style' : 'padding:10px 30px;'}).text.strip()
            content['价格'] = sale.find('span', attrs = {'class' : 'ft-orange'}).text.strip()
            contents.append(content)
        except:
            print('wrong')
    return contents 


def write_html(html):
    with open('2018_9_3_html.txt','a', encoding = 'utf-8') as f:
        f.write(html)



def get_item_name(item_id):
    url = get_history_url(item_id)
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    ###常规操作，做汤
    sales = soup.find_all('tr')    
    item_name = soup.find('span', attrs = {'style' : 'width: 365px;display: inline-block;overflow: hidden;'}).text.strip()
    return item_name
        
    
def send_email_history_prices(item_id):        
    mail_host = 'smtp.163.com'
    mail_user = 'tigertang1998'
    mail_pass = '##passwordhere##'
    sender = 'tigertang1998@163.com'
    receivers = ['1070880522@qq.com']
    content = str(get_history_prices(item_id))
    message = MIMEText(content, 'plain', 'utf-8')   
    message['Subject'] = str(item_id) + '\t' + get_item_name(item_id) +'\t' + 'history prices'
    message['From'] = sender
    message['To'] = receivers[0]
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host,25)
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(
                sender, receivers, message.as_string())
        smtpObj.quit()
        print('success')
    except smtplib.SMTPException as e:
        print('error', e)





