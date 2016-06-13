#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'
"""
    抓取学校赛课上某一课程资源的ppt  需要传入对应资源的url
"""

import requests
from lxml import etree
import threading
import time

def scrapy_ppt(url=None):
    """
    :param url: 需要抓取的页面
    :return:
    """
    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
    }

    # 登陆 获取cookie
    def login(eid, paw):
        """
        :param eid: 学号
        :param paw:  密码
        :return:
        """
        data = {
            'eid':eid,
            'pw':paw,
            'submit':'Login'
        }
        login_url = 'http://elearning.hpu.edu.cn/portal/relogin'

        get_cookie = requests.get(login_url,headers=header)
        header['Cookie'] = get_cookie.cookies.items()[0][0]+'='+get_cookie.cookies.items()[0][1]
        # print get_cookie.cookies.items()[0][0]

        res = requests.post(url = login_url, data=data, headers=header)

    # 下载ppt
    def download_ppt(url, title):
        """
        :param url:  ppt下载地址
        :param title: ppt名
        :return:
        """
        with file(title, 'wb') as f:
            print '-'*10,title,'正在下载'
            f.write(requests.get(url=link, headers=header).content)
            print '-'*10,title,'下载完成'

    eid = raw_input('请输入学号: ')
    pwd = raw_input('请输入密码: ')

    # 登陆
    login(eid, pwd)

    # 分析页面
    res  = requests.get(url=url, headers=header)

    sel = etree.HTML(res.content)

    # print res.content

    # 获取资源页面
    resouce_link = sel.xpath('//div[@class="title"]/a/@href')

    resouce_link = resouce_link[0].replace('tool-reset','tool')

    # 资源页面
    resouce_page = requests.get(url=resouce_link, headers=header)

    sel = etree.HTML(resouce_page.content)
    ppt_links = sel.xpath('//td[@headers="title"]/h4/a[@title="PowerPoint"]')

    # print dir(ppt_links[0])
    for ppt_link in ppt_links:
        title = ppt_link.text.strip()
        link = ppt_link.get('href', None)
        if link is None:
            continue
        new_thread = threading.Thread(target=download_ppt, args=(link, title))
        new_thread.start()
        # new_thread.join()
        # print ppt_links[0].get('href', None)
        # print ppt_links[0].text.strip()



# 资源页面url
url = 'http://elearning.hpu.edu.cn/portal/site/' \
      '34bf9ec8-dfe4-4094-b6f7-05d89998c22c/page/b75edbbc-f08a-4e06-a8d7-a4e707e7141b'

s1 = time.time()
# print s1
scrapy_ppt(url=url)
# threading.Thread().join()
print '用时: ',(time.time()-s1)/60, '分钟'
