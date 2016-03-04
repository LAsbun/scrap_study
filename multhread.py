#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'


import requests
from multiprocessing.dummy import Pool
import time

url_list = []
url = 'http://tieba.baidu.com/p/4361204526?pn=%s'

for i in range(20):
    url_list.append(url %str(i))

def get_souce(url):
    print url
    requests.get(url)

time1  = time.time()
for url in url_list:
    get_souce(url)

print time.time() - time1


po = Pool(4)
time2 = time.time()
res = po.map(get_souce, url_list)
po.close()
po.join()
print time.time() - time2

