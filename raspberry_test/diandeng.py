import RPi.GPIO as GPIO
import time

# 设置GPIO模式
GPIO.setmode(GPIO.BCM)

# 定义GPIO引脚
LED_PIN = 17

# 设置GPIO引脚为输出模式
GPIO.setup(LED_PIN, GPIO.OUT)

try:
    while True:
        # 点亮LED
        GPIO.output(LED_PIN, GPIO.HIGH)
        print("LED on")
        time.sleep(1)  # 等待1秒

        # 熄灭LED
        GPIO.output(LED_PIN, GPIO.LOW)
        print("LED off")
        time.sleep(1)  # 等待1秒

except KeyboardInterrupt:
    # 清理GPIO设置
    GPIO.cleanup()
