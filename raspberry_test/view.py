import cv2
import numpy as np
# center定义
center = 320
"""图像预处理：

将彩色图像转换为灰度图像，这样可以简化后续处理步骤。
使用大津法二值化(cv2.threshold())将灰度图像转换为二值图像，以便将黑色物体与背景分离出来。
对二值图像进行膨胀操作(cv2.dilate())，以填充物体内部的空洞，使物体更连续。
检测黑色物体：

选取图像中特定行(这里是第400行)的像素,检测其中的白色(值为0)像素个数。
如果整行像素全部为白色，则判断摄像头未观察到黑色物体，直接跳过处理。
否则，找到白色像素点的索引，并计算出白色像素的中心位置。
根据白色像素中心与图像中心的偏移量，计算出黑色物体相对于中心的方向。
显示结果：

在控制台输出黑色物体相对于中心的方向。
使用cv2.imshow()显示处理后的图像"""
# 打开摄像头，图像尺寸640*480（长*高），opencv存储值为480*640（行*列）
cap = cv2.VideoCapture(1)
while (1):
    ret, frame = cap.read()
    # 转化为灰度图
    if ret == False:  # 如果是最后一帧这个值为False
       break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 大津法二值化,cvtcolor是将彩色图像转化为灰色图像，frame是彩色图像的意思，cv2.color_BGR2GRAY是灰色图像
    retval, dst = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
    # 膨胀，白区域变大，OTSU算法确定图像的阈值，分割图像  0阈值初始值，超出阈值的新值255
    dst = cv2.dilate(dst, None, iterations=2)
    #  腐蚀，白区域变小、增强白色区域、None是结构元素，是用于图像形态学处理的一个小的图像
    # 它决定了膨胀操作的影响范围和方式，interation=2指示膨胀的次数，
    #膨胀是减少图像在噪声的算法，可以更容易识别图像
    # dst = cv2.erode(dst, None, iterations=6)
    cv2.imshow("dst",dst)

    # 单看第400行的像素值
    color = dst[400]
    # 找到黑色的像素点个数，在这个第400行中的黑色像素的个数,并储存在white_count中
    white_count = np.sum(color == 0)
    # 找到白色的像素点索引
    white_count_judge = np.sum(color == 255)
    #利用这个变量来查找摄像头是否观察到黑色，否则为255则为白色
    #如果全部为白色，则一行的320*2（画面宽度）全为白色的像素点
    if white_count_judge == 640:
        print("黑色像素点为0")
        pass
    else:
        white_index = np.where(color == 0)
        # 防止white_count=0的报错
        #np.where(condition) 是 NumPy 库中的一个函数，找出满足条件 condition 的元素的索引。
        #condition 是 color == 0，表示要找出图像中像素值为0的像素点也就是黑色。
        #当 np.where(color == 0) 执行时，返回一个元组，包含两个数组，分别满足条件的像素点的行索引和列索引
        if white_count == 0:
            white_count = 1
 
        # 找到白色像素的中心点位置
        #(white_index[0][white_count - 1] + white_index[0][0]) 
        #(white_index[0][white_count - 1] 最后一个像素
        #计算了白色像素在水平方向上的范围，即从第一个像素到最后一个像素之间的距离。
        #并求出白色像素的中心位置
        center = (white_index[0][white_count - 1] + white_index[0][0]) / 2
        direction = center - 320
        print(white_index[0][white_count - 1] - white_index[0][0])
        # 计算出center与标准中心点的偏移量
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
# 释放清理
cap.release()
cv2.destroyAllWindows()
 
 