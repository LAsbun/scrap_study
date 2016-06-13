#!/usr/bin/env python
# -*- coding: utf-8 -*-
# LAsbun  @ 2016-03-13

from urllib import urlopen

from bs4 import BeautifulSoup
import datetime
import random
import re

random.seed(datetime.datetime.now())

def getLinks(articleUrl):
    html = urlopen('https://en.wikipedia.org'+articleUrl)
    bsobj = BeautifulSoup(html, 'lxml')
    return bsobj.find('div',{'id':'bodyContent'}).findAll('a', href=re.compile("^(/wiki/)((?!:).)*$"))

links = getLinks('/wiki/Kevin_Bacon')
while len(links) > 0:
    newArticle = links[random.randint(0, len(links)-1)].attrs['href']
    print newArticle
    links = getLinks(newArticle)

