#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'

import requests
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool
import lxml
import random
import sys
import time
reload(sys)
sys.setdefaultencoding('utf8')

filename = 'book.txt'
file_content = ''
file_content += '生成时间： '+ time.asctime()

headers = [
        {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
        {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
        {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
        {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},
        {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}
]

def get_summary(url):

    summary_content = ''

    source_code = requests.get(url, headers=random.choice(headers))

    plain_text = source_code.text

    soup = BeautifulSoup(plain_text, 'lxml')

    soup_list = soup.find('div', {'class':'intro'}).get_text()


    summary_content += '%s' %(soup_list)
    return summary_content

def get_book(url):

    global headers

    # url = 'https://www.douban.com/tag/%s/?focus=book' %(book_tag)#'https://www.douban.com/tag/%E5%B0%8F%E8%AF%B4/?focus=book'#raw_input('url: ')
    source_code = requests.get(url, headers=random.choice(headers))

    plain_text = source_code.text

    soup = BeautifulSoup(plain_text, "lxml")

    file_content = ''

    #print soup

    #file_content += "\n\n---" + book_tag

    count = 1

    list_soup = soup.find('div', {'class' : 'mod-list book-list'})

    #print list_soup

    for book_info in list_soup.findAll('dd'):
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

        file_content += "*%d\t<%s>\t评分：%s\n\t%s\n\t%s\n%s\n\n" % (
            count, title, rating, author_info.strip(), pub_info.strip(), summary
        )
        count += 1

        return file_content


def do_sth(book_list):

    book_url_list = []

    for book in book_list:
        url = 'https://www.douban.com/tag/%s/?focus=book' %(book)
        book_url_list.append(url)

    po = Pool(4)
    res  = po.map(get_book, book_url_list)

    for i in res:
        print i


if __name__ == '__main__':
    time1 = time.time()
    book_lists = ['心理学', '人物传记', '中国历史', '旅行', '生活', '科普']

    do_sth(book_lists)

    # f = open(filename, "w")
    # f.write(file_content)
    # f.close()
    tim2 = time.time()

    print tim2-time1
















