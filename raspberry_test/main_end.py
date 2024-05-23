import threading
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

motor_pin1 = 21
motor_pin2 = 20
motor_pin3 = 16
motor_pin4 = 12

import cv2
import numpy as np

GPIO.setup(motor_pin1, GPIO.OUT)
GPIO.setup(motor_pin2, GPIO.OUT)
GPIO.setup(motor_pin3, GPIO.OUT)
GPIO.setup(motor_pin4, GPIO.OUT)

pwm_1 = GPIO.PWM(motor_pin1, 500)  
pwm_2 = GPIO.PWM(motor_pin2, 500)  
pwm_3 = GPIO.PWM(motor_pin3, 500)  
pwm_4 = GPIO.PWM(motor_pin4, 500)  

pwm_1.start(0)
pwm_2.start(0)
pwm_3.start(0)
pwm_4.start(0)

def set_motor_speed(pwm, speed):
    pwm.ChangeDutyCycle(speed)

move1=20
move2=22    

def move_forward(move1,move2):
    set_motor_speed(pwm_1, move1)
    set_motor_speed(pwm_2, 0)
    set_motor_speed(pwm_3, move2)
    set_motor_speed(pwm_4, 0)

def turn_left():
    set_motor_speed(pwm_1, 0)
    set_motor_speed(pwm_2, 37)
    set_motor_speed(pwm_3, 35)
    set_motor_speed(pwm_4, 0)

def turn_right():
    set_motor_speed(pwm_1, 28)
    set_motor_speed(pwm_2, 0)
    set_motor_speed(pwm_3, 0)
    set_motor_speed(pwm_4, 32)

def move_backward():
    set_motor_speed(pwm_1, 0)
    set_motor_speed(pwm_2, 25)
    set_motor_speed(pwm_3, 0)
    set_motor_speed(pwm_4, 28)

def stop_motors():
    set_motor_speed(pwm_1, 0)
    set_motor_speed(pwm_2, 0)
    set_motor_speed(pwm_3, 0)
    set_motor_speed(pwm_4, 0)

def drive(direction):
    global c3
    if(np.sum(color==0)==640 and c3==1):
        turn_right()
        time.sleep(1.8)
        move_forward(move1,move2)
        time.sleep(2.5)
        c3=2     
        stop_motors()
        time.sleep(1)
    elif(direction < 60 and direction > -60):
        move_forward(move1,move2)
    elif (direction >= 60 and direction < 320):
        turn_right()
    elif (direction <= -60):
        turn_left()

def drive2(direction):
    global c4
    if(np.sum(color==0)<600 and np.sum(color == 0)>500 and c4==1):
        move_forward(move1,move2)
        time.sleep(0.5)
        turn_left()
        time.sleep(0.85)
        move_forward(move1,move2)
        time.sleep(5)
        stop_motors()
        time.sleep(10)
        c4=2     
    elif(direction < 60 and direction > -60):
        move_forward(move1,move2)
    elif (direction >= 60 and direction < 320):
        turn_right()
    elif (direction <= -60):
        turn_left()    

    
        

center = 320
c1=1
c2=1
c3=1
c4=1

cap = cv2.VideoCapture(0)  ##

while (1):
    ret, frame = cap.read()
    # 转化为灰度图
    if ret == False:  # 如果是最后一帧这个值为False
       break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 大津法二值化
    retval, dst = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
    # 膨胀，白区域变大
    dst = cv2.dilate(dst, None, iterations=2)
    # # 腐蚀，白区域变小
    # dst = cv2.erode(dst, None, iterations=6)
    #cv2.imshow("dst",dst)  ##

    # 单看第400行的像素值
    color = dst[400]
    # 找到白色的像素点个数
    white_count = np.sum(color == 0)
    # 找到白色的像素点索引
    white_count_judge = np.sum(color == 255)#利用这个变量来查找摄像头是否观察到黑色
    if white_count_judge == 640:
        print("黑色像素点为0")

    else:
        white_index = np.where(color == 0)
        # 防止white_count=0的报错
        if white_count == 0:
            white_count = 1
 
        # 找到白色像素的中心点位置
        center = (white_index[0][white_count - 1] + white_index[0][0]) / 2
        direction = center - 320
        print(direction)
        # 计算出center与标准中心点的偏移量
    if(c3==2):
        c3=3
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if(c2==1):
        move_forward(move1,move2)
        time.sleep(1)
        c2=0
        move1=17
        move2=19    
    
    drive(direction)

while(c3==3):
    ret, frame = cap.read()
    # 转化为灰度图
    if ret == False:  # 如果是最后一帧这个值为False
       break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 大津法二值化
    retval, dst = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
    # 膨胀，白区域变大
    dst = cv2.dilate(dst, None, iterations=2)
    # # 腐蚀，白区域变小
    # dst = cv2.erode(dst, None, iterations=6)
    #cv2.imshow("dst",dst)  ##

    # 单看第400行的像素值
    color = dst[400]
    # 找到白色的像素点个数
    white_count = np.sum(color == 0)
    # 找到白色的像素点索引
    white_count_judge = np.sum(color == 255)#利用这个变量来查找摄像头是否观察到黑色
    if white_count_judge == 640:
        print("黑色像素点为0")

    else:
        white_index = np.where(color == 0)
        # 防止white_count=0的报错
        if white_count == 0:
            white_count = 1
 
        # 找到白色像素的中心点位置
        center = (white_index[0][white_count - 1] + white_index[0][0]) / 2
        direction = center - 320
        print(direction)
        # 计算出center与标准中心点的偏移量

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    drive2(direction)    
    
 
# 释放清理
cap.release()
cv2.destroyAllWindows()