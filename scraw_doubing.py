#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'

'''
抓取豆饼表情
'''

import requests
from lxml import etree
# 把str编码由ascii改为utf8（或gb18030）
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def get_image(name):
    data = {
        'Host':"www.doubean.com",
        'ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$TextBoxTextLine1':name,
        'ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$ButtonMake':"生成图！",
        'ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$TextBoxPost':"",

        'Cookie':"ASP.NET_SessionId=wdfzby55yboklv55aqj0pnet; Hm_lvt_61eade8a2455844e3d0c428663e04daf=1460959172; Hm_lpvt_61eade8a2455844e3d0c428663e04daf=1460959188",

        '__EVENTVALIDATION':"/wEWBwLwrpr5CgKEyvnFBwLsk9+8AgLRgaafBwKEqobnAwLRl8/1CwKblfuYCayBhLqGZYEFTVvZ9YYKZkh0B3rb",
        '__VIEWSTATEGENERATOR':"5A19DEE9",
        '__VIEWSTATE':"/wEPDwULLTExNzc1MzU5NTUPZBYCZg9kFgJmD2QWBAIBD2QWAgITD2QWAmYPZBYEAgEPFgIeB2NvbnRlbnQFJOW8oOWtpuWPi+S4i+i3quWcqOe6v+ihqOaDheeUn+aIkOWZqGQCAw8WAh8ABbAB5byg5a2m5Y+L5LiL6Leq6KGo5oOF55Sf5oiQ5ZmoLOihqOaDheeUn+aIkCzooajmg4XliLbkvZws5Zyo57q/6KGo5oOF55Sf5oiQLOWcqOe6v+ihqOaDheWItuS9nCzlnKjnur/ooajmg4XnlJ/miJDlmags5Zu+54mH55Sf5oiQ5ZmoLOWcqOe6v+WbvueJh+eUn+aIkOWZqCzmtYHooYzlm77niYfnlJ/miJDlmahkAgMPZBYCAhEPZBYCAg0PZBYmAgMPFgIeCWlubmVyaHRtbAUP5byg5a2m5Y+L5LiL6LeqZAIFD2QWBAIBDw8WAh4EVGV4dAVFPGEgaWQ9ImF1dGhvci1saW5rIiBhdXRob3I9IjEiPjxzcGFuIGNsYXNzPSJhdXRob3IiPuixhuixhjwvc3Bhbj48L2E+ZGQCBQ8PFgQfAgUM5pyA6LWe6KGo5oOFHgtOYXZpZ2F0ZVVybAURTGlrZS5hc3B4P2lkPTE2NDBkZAIHD2QWBAIBDw8WAh8CBQ/nrKzkuIDooYzmloflrZdkZAIDDw8WAh4JTWF4TGVuZ3RoAkBkZAIJDxYCHgdWaXNpYmxlaBYCAgMPDxYCHwJlZGQCCw8WAh8FaBYCAgMPDxYCHwJlZGQCDQ8WAh8FaBYCAgMPDxYCHwJlZGQCDw8WAh8FaBYCAgMPDxYCHwJlZGQCFQ8PFgIeCEltYWdlVXJsBTp+L2ZhY2Uvc3RvcmUvZmFjZS8wMDAwMDAxNjQwLy9tYWtlLmpwZz9jPTIwMTYwNDE4MTM1OTExOTE3FgIeBXN0eWxlBRV3aWR0aDoxOTg7aGVpZ2h0OjE5NjtkAhcPDxYCHwIFATBkZAIZDw8WAh8CBQVGYWxzZWRkAhsPEGQPFgVmAgECAgIDAgQWBQUV6LCi6ICB5aSn5LiN5p2A5LmL5oGpZWVlZRYAZAIhDw8WAh8CBQUxNTgxN2RkAiMPDxYCHwIFBDQwOTlkZAIlDw8WAh8CBRMyMDE2LTA0LTE4IDEzOjU5OjExZGQCJw8PFgIfAgUCMjFkZAItDxYCHwIF8gk8bGk+PGEgaHJlZj0ibWFrZS5hc3B4P2lkPTE2NTUiPumHkemmhumVv+eci+eUteiEkTwvYT48L2xpPjxsaT48YSBocmVmPSJtYWtlLmFzcHg/aWQ9MTExIj7mlZnnmofkuYvlsI/nu7Xnvorllp3ojLY8L2E+PC9saT48bGk+PGEgaHJlZj0ibWFrZS5hc3B4P2lkPTQ5MyI+55uf5ZOp5ZOp5oyB546r55GwPC9hPjwvbGk+PGxpIGNsYXNzPSJjdXJyZW50Ij48YSBocmVmPSJtYWtlLmFzcHg/aWQ9MTY0MCI+5byg5a2m5Y+L5LiL6LeqPC9hPjwvbGk+PGxpPjxhIGhyZWY9Im1ha2UuYXNweD9pZD0xNDg4Ij7ph5Hppobplb/nhornjKvlpLRESVNDT+eZu+WcujwvYT48L2xpPjxsaT48YSBocmVmPSJtYWtlLmFzcHg/aWQ9NDM5Ij7ph5Hppobplb/nhornjKvlpLTmiLTpkqLnm5TmjIHngavnrq3lvLk8L2E+PC9saT48bGk+PGEgaHJlZj0ibWFrZS5hc3B4P2lkPTI0OSI+6LW15pys5bGx6K6t5Lq6PC9hPjwvbGk+PGxpPjxhIGhyZWY9Im1ha2UuYXNweD9pZD0xNTI0Ij7mlZnnmofog5blqIPmir3ng588L2E+PC9saT48bGk+PGEgaHJlZj0ibWFrZS5hc3B4P2lkPTE3MTEiPumHkemmhumVv+aKq+iiq+WtkDwvYT48L2xpPjxsaT48YSBocmVmPSJtYWtlLmFzcHg/aWQ9MTgxNyI+5Zad57+U5pel5ZKM6IS4PC9hPjwvbGk+PGxpPjxhIGhyZWY9Im1ha2UuYXNweD9pZD0xNjg4Ij7lvKDlrablj4vlgZrlub/mkq3kvZPmk408L2E+PC9saT48bGk+PGEgaHJlZj0ibWFrZS5hc3B4P2lkPTE5NCI+5byg5a2m5Y+L54aK54yr5aS05Y+z5oyHPC9hPjwvbGk+PGxpPjxhIGhyZWY9Im1ha2UuYXNweD9pZD0xNTgwIj7ok53ooaPkuozom4vmlZnnmoc8L2E+PC9saT48bGk+PGEgaHJlZj0ibWFrZS5hc3B4P2lkPTE3MjQiPuWViu+8jOaYr+WQl++8jOi+o+acqOajkjwvYT48L2xpPjxsaT48YSBocmVmPSJtYWtlLmFzcHg/aWQ9MTc5OSI+5oiR5Lmf5piv6YaJ5LqGPC9hPjwvbGk+PGxpPjxhIGhyZWY9Im1ha2UuYXNweD9pZD02NTciPuaVmeeah+eMq+WSquWWnemlruaWmTwvYT48L2xpPjxsaT48YSBocmVmPSJtYWtlLmFzcHg/aWQ9MTc3MCI+5a2k54us55qE5ZCD5bGO54uXPC9hPjwvbGk+PGxpPjxhIGhyZWY9Im1ha2UuYXNweD9pZD0xNDQ4Ij7ph5Hppobplb/nhornjKvlpLTmjIHonJjom5vnjovpnq3ngq7mgJLmjIc8L2E+PC9saT48bGk+PGEgaHJlZj0ibWFrZS5hc3B4P2lkPTk5NCI+5byg5a2m5Y+L54aK54yr5aS05oyB6K+BPC9hPjwvbGk+PGxpPjxhIGhyZWY9Im1ha2UuYXNweD9pZD0xNTcwIj7lvKDlrablj4vooqvlkYrkuro8L2E+PC9saT5kAi8PFgIfAgXRAjxhIGhyZWY9ImphdmFzY3JpcHQ6dm9pZCgwKTsiPjE8L2E+PHNwYW4gY2xhc3M9InBhZ2UtYnJlYWsiPi4uLjwvc3Bhbj48YSBocmVmPSJqYXZhc2NyaXB0OnZvaWQoMCk7Ij4xODwvYT48YSBocmVmPSJqYXZhc2NyaXB0OnZvaWQoMCk7Ij4xOTwvYT48YSBocmVmPSJqYXZhc2NyaXB0OnZvaWQoMCk7IiBjbGFzcz0iY3VycmVudCI+MjA8L2E+PGEgaHJlZj0iamF2YXNjcmlwdDp2b2lkKDApOyI+MjE8L2E+PGEgaHJlZj0iamF2YXNjcmlwdDp2b2lkKDApOyI+MjI8L2E+PHNwYW4gY2xhc3M9InBhZ2UtYnJlYWsiPi4uLjwvc3Bhbj48YSBocmVmPSJqYXZhc2NyaXB0OnZvaWQoMCk7Ij45NDwvYT5kAjcPFgIfAmVkAjkPFgIfAmVkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBUBjdGwwMCRjdGwwMCRDb250ZW50UGxhY2VIb2xkZXIxJENvbnRlbnRQbGFjZUhvbGRlcjEkQ2hlY2tCb3hGbGlwITI/BhoJFjGbGm++WFts3t+dcVs=",

    }
    url = 'http://www.doubean.com/face/Make.aspx?id=1640&textid=140167'
    headers = {'Referer':"http://www.doubean.com/face/Make.aspx?id=1640&textid=140167",
        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0"}

    tt = requests.post(url=url, data=data, headers=headers)

    hh = etree.HTML(tt.content)

    imag = hh.xpath('//*[@id="ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolder1_ImageResult"]')

    print imag[0].attrib['src']

    ress = requests.get('http://www.doubean.com/face/'+imag[0].attrib['src'])

    print '正在下载豆饼表情-----' + imag[0].attrib['src'].split(r'=')[1]

    with open(name+'.jpg', 'w') as f:
        f.write(ress.content)

    print '----Done----'

# print tt.content

name = raw_input('>')
get_image(name=name)
