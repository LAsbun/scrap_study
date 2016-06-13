#!/usr/bin/env python
# -*- coding: utf-8 -*-
# LAsbun  @ 2016-03-13
"""
任意的网址
"""

from urllib import urlopen

from bs4 import BeautifulSoup

import random

import re

import datetime

pages = set()
random.seed(datetime.datetime.now())

#Retrieve a list of all Internal links found on pages
def getInternalLinks(bsobj, includeUrl):
    internalLinks = []

    for link in bsobj.findAll('a', href=re.compile("^(/|.*"+includeUrl+")")):
        getlinkurl = link.attrs['href']
        if getlinkurl is not None:
            if getlinkurl not in internalLinks:
                internalLinks.append(getlinkurl)

    return internalLinks

#Retrieve a list of all external links found on page
def getExternalLinks(bsobj, excludeUrl):
    externalLinks = []
    for link  in bsobj.findAll("a", href=re.compile("^(http|www)((?!"+excludeUrl+").)*$")):
        gettemplink = link.attrs['href']
        if gettemplink is not None:
            if gettemplink not in externalLinks:
                externalLinks.append(gettemplink)

    return externalLinks

def splitAddress(address):
    
    try:
        addressParts = address.replace('http://', '').split('/')
    except  Exception:
        addressParts = address.replace('https://', '').split('/')
    return addressParts

def getRandonExternalLink(startingPage):
    html = urlopen(startingPage)

    bsobj = BeautifulSoup(html,'lxml')
    
    #print bsobj

    externalLinks = getExternalLinks(bsobj, splitAddress(startingPage)[0])
    
    if len(externalLinks) == 0:
        internalLinks = getInternalLinks(startingPage)
        return getExternalLinks(internalLinks[random.randint(0,len(internalLinks)-1)])
    
    else:
        return externalLinks[random.randint(0, len(externalLinks)-1)]


def followExternalOnly(startingSite):
    
    externalLink = getRandonExternalLink(startingSite)

    print "random external link is: "+ externalLink

    followExternalOnly(externalLink)

followExternalOnly('http://oreilly.com')
