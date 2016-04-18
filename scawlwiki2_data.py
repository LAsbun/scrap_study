#!/usr/bin/env python
# -*- coding: utf-8 -*-
# LAsbun  @ 2016-03-13

from urllib import urlopen

from bs4 import BeautifulSoup

import re

pages = set()

def getLInks(pageUrl):
    global pages
    html = urlopen("http://en.wikipedia.org"+pageUrl)

    bsobj = BeautifulSoup(html, 'lxml')

    try:
        print bsobj.h1.get_text()
        print bsobj.find(id='mw-content-text').findAll('p')[0]
        print bsobj.find(id='ca-edit').find('span').find('a').attrs['href']
    except AttributeError:
        print 'this page is missing something!'

    for link in bsobj.findAll('a', href=re.compile('^(/wiki/)')):
            if 'href' in link.attrs:
                if link.attrs['href'] not in pages:
                    newPage = link.attrs['href']
                    print '-------\n' + newPage
                    pages.add(newPage)
                    getLInks(newPage)
getLInks('')



