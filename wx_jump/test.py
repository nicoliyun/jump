#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:liyun

astr = 'adb shell input swipe 320 410 320 410 {}'.format(int(1.35))
cmd = 'adb shell input swipe 320 410 320 410 ' + str(1.35)
print astr
print cmd