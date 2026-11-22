# MicroPython の machine　モジュールからPinという機能を読み込む
from machine import Pin

import time
ir =  Pin(16, Pin.IN, Pin.PULL_UP)  # GPIO16を入力モードに設定し、プルアップ抵抗を有効化

while True:
    if ir.value() == 0:  # 受信中か
        print("赤外線信号を受信しました")  # メッセージを表示
        time.sleep_ms(100)