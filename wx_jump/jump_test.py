#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:liyun
import time
import PIL
import numpy
import matplotlib.pyplot as plt
import os
# import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
# 是否需要更新截图的开关

need_update = True

def get_screen_image():
    # 获取当前屏幕截图
    os.system('adb shell screencap -p /sdcard/wechat_jump.png')
    # 将图片发送至代码所在目录下
    os.system('adb pull /sdcard/wechat_jump.png')
    # 返回图像数据
    return numpy.array(PIL.Image.open('wechat_jump.png'))
def jump_to_next(point1, point2):
    # 分别获取第一下点击鼠标和第二下点击鼠标的坐标值
    x1, y1 = point1
    x2, y2 = point2
    # 计算第一下点击鼠标和第二下点击鼠标之间的像素距离
    distance = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
    print x1,x2,y1,y2,distance
    # 模拟按压屏幕，前两个数字是点击屏幕起始坐标，三四个数字是点击屏幕的终止坐标，最后一个数字是按压时间，需要自己测试
    os.system('adb shell input swipe 320 410 320 410'+str(distance*1.35))

def click(event, coor=[]):
    global need_update
    print "click----" + str(need_update)
    # 获取鼠标点击点的坐标值，以元组形式添加至坐标列表
    coor.append((event.xdata, event.ydata))
    print len(coor)
    # 直到点了两下屏幕，开始调用鼠标点击函数
    if len(coor)==2:
        jump_to_next(coor.pop(), coor.pop())
    # 打开更新截图开关，更新截图开关后，图片才可更新
    need_update = True

def update_screen(frame):
    global need_update
    print "update----"+str(need_update)
    if need_update:
        time.sleep(3)
        #更新截图
        myimage.set_array(get_screen_image())
        #关闭更新截图开关
        need_update = False
    #返回元组数据
    return myimage,
#以指定尺寸创建一块画布
# figure = plt.figure(figsize=(6, 8))
figure = plt.figure()
#用得到的图像数据在画布上复制出截图
myimage = plt.imshow(get_screen_image(), animated=True)
#使画布上的画更加紧凑
# plt.tight_layout()
#将鼠标点击事件与click函数绑定
figure.canvas.mpl_connect('button_press_event',click)
#更新截图
ani = FuncAnimation(figure, update_screen, interval=50, blit=True)
#显示图片
plt.show()