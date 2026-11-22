from machine import Pin
import time

ir_led = Pin(15, Pin.OUT, value=0)  # GPIO15を出力モードに設定し、初期値を0に設定

while True:
    ir_led.on()
    time.sleep(0.5)  # 0.5秒待機
    ir_led.off()
    time.sleep(0.5)  # 0.5秒待機