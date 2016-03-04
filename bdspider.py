#! /usr/bin/env python
#coding:utf-8

import requests
from lxml import etree
import json
import time
from multiprocessing.dummy import Pool

import sys

reload(sys)

sys.setdefaultencoding("utf8")

# 爬取百度贴吧某一贴前20页回复
# 用lxml


f = open("bd.txt", "w")

def writetofile(item):
    f.writelines("--回帖人姓名%s\n" %str(item['user_name']))
    f.writelines("--回帖人时间%s\n" %str(item['date']))
    f.writelines("--回帖人内容%s\n\n" %str(item['reply_content']))


def get_content(url):

    html = requests.get(url)

    html = etree.HTML(html.text)

    content_list = html.xpath('//div[@class="l_post j_l_post l_post_bright  "]')

    item = {}

    for info in content_list:
        reply_info = json.loads(info.xpath('@data-field')[0])
        author = reply_info['author']['user_name']
        reply_time = reply_info['content']['date']
        reply_content = info.xpath('div[@class="d_post_content_main"]/div/cc/div[@class="d_post_content j_d_post_content  clearfix"]/text()')[0].strip()

        item['user_name'] = author
        item['date'] = reply_time
        item['reply_content'] = reply_content

        print item
        writetofile(item)



def geturl():

    url_list = []



    for i in range(1,21):
        url_list.append("http://tieba.baidu.com/p/3522395718?pn=%s" %str(i))


    po = Pool(4)

    res = po.map(get_content, url_list)
    po.close()
    po.join()





if __name__ == "__main__":



    geturl()

    f.close()