# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 20:13:49 2018

@author: TIGER
"""

'''
爬dota2比赛数据
'''

import requests
from bs4 import BeautifulSoup
import time

def get_html(url):
    r = requests.get(url)
    r.encoding='utf-8'
    return r.text

contents = []

def get_content(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    liTags = soup.find_all('div', attrs={'class': 'match-event event with-score is-not-live'})
    
    for div in liTags:
        content = {}
        try:
            content['team1'] = div.find('div', attrs = {'class': 'team-home'}).text.strip()
            content['team2'] = div.find('div', attrs = {'class': 'team-away'}).text.strip()
            content['score'] = div.find('div', attrs = {'class': 'event-main-scores'}).text.strip()
            contents.append(content)
        except:
            print('div出问题')
    return contents

f = open("html.txt", "a", encoding = 'utf-8')
f.write(html)

#e.g.http://esportlivescore.com/ra_2018-the-international.html


