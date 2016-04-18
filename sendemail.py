#!/usr/bin/env python
#encoding: utf-8
#LAsbun  @ 2016-04-06


import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 第三方 SMTP 服务
mail_host="smtp.xxxx.com"  #设置服务器
mail_user="useremail"    #用户名
mail_pass="passwd"   #口令


sender = 'useremail'
receivers = 'receriveremail'  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
message['From'] = sender
message['To'] = receivers

subject = 'Python SMTP 邮件测试'
message['Subject'] = Header(subject, 'utf-8')


try:
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
    smtpObj.login(mail_user,mail_pass)
    print 's'
    smtpObj.sendmail(sender, receivers, message.as_string())
    print "邮件发送成功"
except smtplib.SMTPException, e:
    print "Error: 无法发送邮件"
    print e

