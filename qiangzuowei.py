import os
import sys
import random
import time
import datetime
from PIL import Image
from PIL import ImageGrab
import pyautogui
import cv2
import random
screenshot_loc = './1.png'
yuyueDict = {'1':[521,316,619,374],'2':[650,315,747,373],'3':[780,314,878,374],'4':[910,316,1010,374]}
clickDict = {'1':[574,352],'2':[697,343],'3':[818,347],'4':[957,348]}
yuyueloc = 910,316,1010,374
yuyueloc1 = 521,316,619,374
clickloc = 958,347
randomLoc = 677,507
#yuyueloc = 654,316,741,366
#clickloc = 706,364
def CompareImage(filepath1,filepath2):
    image1 = cv2.imread(filepath1)
    image2 = cv2.imread(filepath2)
    result = cv2.matchTemplate(image1,image2,cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    x,y = max_loc
    return x,y,max_val

def screenshot(x1=0,y1=0,x2=2000,y2=2000, screen_type='all'):
    if screen_type == 'all':
        img = ImageGrab.grab()
        img.save(screenshot_loc)
    else:
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        img.save(screenshot_loc)

def ClickPicAndConfirm(click_pic, confirm_pic, sleep_time = 0.2, screens = None):
    x,y,max_val = CompareImage(screenshot_loc, click_pic)
    pyautogui.leftClick(x=x+10, y=y+10, interval=0.0, duration=0.0)
    print('clickloc',x+10,y+10)
    time.sleep(sleep_time)
    for i in range(0,10):
        if screens == None:
            screenshot()
        else:
            x1 = screens[0]
            y1 = screens[1]
            x2 = screens[2]
            y2 = screens[3]
            screenshot(x1, y1, x2, y2)
        x,y,max_val = CompareImage(screenshot_loc, confirm_pic)
        if max_val > 0.9:
            return max_val
            break
        time.sleep(sleep_time)
    return max_val

def WaitTime(day = 7, hour = -1):
    localtime = time.localtime(time.time())
    times = random.randint(3600,7200)
    i = 0
    print(localtime.tm_mday,localtime.tm_hour)
    nowday = 0
    nowhour = 0
    while nowday < day or nowhour < hour:
        time.sleep(1)
        localtime = datetime.datetime.now()
        nowday = int(localtime.strftime("%d"))
        nowhour = int(localtime.strftime("%H"))
        print(nowday, nowhour)
        #localtime = time.localtime(datetime.datetime.now())
        i = i + 1
        if i % 60 == 0:
            print(localtime,times,i)
        if i > times:
            pyautogui.press('f5')
            times = random.randint(3600,7200)
            i = 0
            print('刷新了')
            print(localtime,times,i)

def ClickMouseAndCheck(x=clickloc[0], y=clickloc[1], confirm_pic='./dianjiyuyue.PNG'):
    pyautogui.leftClick(x=x, y=y, interval=0.0, duration=0.0)
    print('ClickMouseAndCheck',x,y)
    for i in range(0,5):
        screenshot()
        x,y,max_val = CompareImage(screenshot_loc, confirm_pic)
        if max_val > 0.9:
            return max_val
            break
            time.sleep(0.1)
    return max_val

def confirm(confirm_pic1 = './yiyueman.PNG', confirm_pic2 = './yuyueshijian.PNG', which = '4', looptimes = 400, sleepchoice = 'short'):
    i = 0
    while i < looptimes:
        print('confirm')
        yuyuepic = yuyueDict[which]
        x1 = yuyuepic[0]
        y1 = yuyuepic[1]
        x2 = yuyuepic[2]
        y2 = yuyuepic[3]
        screenshot(x1, y1, x2, y2, screen_type = 'no')
        x,y,max_val = CompareImage(screenshot_loc, confirm_pic1)
        if max_val > 0.9:
            pyautogui.leftClick(x=randomLoc[0]+10, y=randomLoc[1]+10, interval=0.0, duration=0.0)
            pyautogui.press('f5')
            if sleepchoice == 'short':
                sleeptime = 2
            else:
                print('约满了，继续刷新')
                sleeptime = random.randint(60,80)
            time.sleep(sleeptime)
            i = i + 1
            #print('约满了')
            continue
        x,y,max_val = CompareImage(screenshot_loc, confirm_pic2)
        if max_val > 0.9:
            print('有位置')
            return True

        x,y,max_val = CompareImage(screenshot_loc, './yiyuyue.png')
        if max_val > 0.9:
            print('预约成功位置')
            return False
        else:
            pyautogui.leftClick(x=randomLoc[0]+10, y=randomLoc[1]+10, interval=0.0, duration=0.0)
            pyautogui.press('f5')
            i = i + 1
            print(max_val)
            time.sleep(2)
    return False

def Preorder(day, hour=7, clickMouse='4', which = '4'):
    clickLock = clickDict[clickMouse]
    while True:
        print('这个是提前抢周六周日的！！要多敲几个回车！！！！还有时间要设置正确！！！')
        pyautogui.leftClick(x=randomLoc[0]+10, y=randomLoc[1]+10, interval=0.0, duration=0.0)
        pyautogui.press('f5')
        WaitTime(day, hour)
        pyautogui.leftClick(x=randomLoc[0]+10, y=randomLoc[1]+10, interval=0.0, duration=0.0)
        pyautogui.press('f5')
        max_val = 0
        time.sleep(0.3)
        hasLoc = confirm(confirm_pic1 = './yiyueman.PNG', confirm_pic2 = './yuyueshijian.PNG', which = which, looptimes = 2000000, sleepchoice = 'long')
        if hasLoc != True:
            print('没有位置')
            break
        while ClickMouseAndCheck(clickLock[0], clickLock[1]) < 0.9:
            continue
        while ClickPicAndConfirm('./tijiaoyuyue.png', './queding.png') < 0.9:
            continue
        while ClickPicAndConfirm('./queding.png', './yiyuyue.png', 20) < 0.9:
            continue
        break

def order(which = '3'):
    clickLock = clickDict[which]
    while True:
        print('这个是刷的！！！注意点确定的位置！！！注意图片位置！！！要多敲几个回车！！！！')
        pyautogui.press('enter')
        time.sleep(2)
        pyautogui.leftClick(x=randomLoc[0]+10, y=randomLoc[1]+10, interval=0.0, duration=0.0)
        pyautogui.press('f5')
        max_val = 0
        time.sleep(0.3)
        hasLoc = confirm(confirm_pic1 = './yiyueman.PNG', confirm_pic2 = './yuyueshijian.PNG', which = which, looptimes = 2000000, sleepchoice = 'long')
        if hasLoc != True:
            print('没有位置')
            break
        while ClickMouseAndCheck(clickLock[0],clickLock[1]) < 0.9:
            continue
        while ClickPicAndConfirm('./tijiaoyuyue.png', './queding.png') < 0.9:
            continue
        while ClickPicAndConfirm('./queding.png', './yiyuyue.png', 20, yuyueDict[which]) < 0.9:
            continue
        break

order(which = '3') #实时抢，哪天都抢，疯狂刷票
#Preorder(day = 9, hour = 20, clickMouse = '3', which = '3') #专抢周六周日的