#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:liyun

astr = 'adb shell input swipe 320 410 320 410 {}'.format(int(1.35))
cmd = 'adb shell input swipe 320 410 320 410 ' + str(1.35)
print astr
print cmd

keym = {"a":"123","b":"345","c":"567"}
print keym["a"]


bizContent = {"merchantTradeNo":"12356564","totalAmount":"5200.00","productCode":"30100501","userId":"${userId}","merchantExtParams":"rereerer"}

bizContents = {"merchantTradeNo":"TEST-20180127095408416-1VUaVVgV","productCode":"30100501","totalAmount":999,"userId":3172}


