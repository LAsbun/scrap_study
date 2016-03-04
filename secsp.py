#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'

# """
#
# 用多线程爬取豆瓣各标签页的前几本书
# 书名，评分，摘要，作者，译者，以及出版信息和价格
#
# 相比单线程而言多线程（开了4个线程池）快了3倍，不过还是很慢 27.325056076
#
# IDE: PYCHARM
# HTMLPARSER:LXML,BEAUTIFULSOUP
#
# """


from multiprocessing.dummy import Pool
import requests
import time
import random
from bs4 import BeautifulSoup

# 防止报UnicodeDecodeError  -_-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# global variety

headers = [
        {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
        {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
        {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
        {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},
        {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}
]

# 将爬取的所有的内容存进一个文档中
def get_content(book_list):
    """
    :param book_list:  各种标签
    :return: 无
    """
    po = Pool(4)
    res = po.map(get_book, book_list)
    with open("book.txt", "w") as f:
        for i in res:
            print i
            f.write(i)

# 抓取某一本书的摘要
def get_summary(url):
    """
    :param url: 要爬取的url
    :return: 返回摘要
    """

    summary_content = ''

    source_code = requests.get(url, headers=random.choice(headers))

    plain_text = source_code.text

    soup = BeautifulSoup(plain_text, 'lxml')

    soup_list = soup.find('div', {'class':'intro'}).get_text()


    summary_content += '%s' %(soup_list)
    return summary_content

# 得到书名，评分，作者等主要内容
def get_book(book):

    url = 'https://www.douban.com/tag/%s/?focus=book' %(book)

    html = requests.get(url, headers=random.choice(headers)).text

    bsoup = BeautifulSoup(html, "lxml")

    temp_div = bsoup.find('div', {'class':'mod-list book-list'})

    count = 1

    cate_content = '---%s----\n\n' %(book)

    for book_info in temp_div.findAll('dd'):
        title = book_info.find('a', {'class':'title'}).string.strip()
        desc_list = book_info.find('div', {'class':'desc'}).string.strip().split('/')
        author_info = '作者/译者: ' + '/'.join(desc_list[0:-3])
        pub_info = '出版信息: ' + '/'.join(desc_list[-3:])
        try:
            rating = book_info.find('span', {'class':'rating_nums'}).string.strip()
        except Exception, e:
            rating = '无'


        try:
            url = book_info.find('a', {'class':'title'})['href']
            #print url
            summary = get_summary(url)
        except Exception, e:
            summary = '无'

        cate_content += "*%d\t<%s>\t评分：%s\n\t%s\n\t%s\n%s\n\n" % (
            count, title, rating, author_info.strip(), pub_info.strip(), summary
        )
        count += 1

    return cate_content



if __name__ == "__main__":

    time1 = time.time()
    book_lists = ['心理学', '人物传记', '中国历史', '旅行', '生活', '科普']

    get_content(book_lists)

    tim2 = time.time()

    print tim2-time1
