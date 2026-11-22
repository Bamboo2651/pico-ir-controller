# MicroPython の machine　モジュールからPinという機能を読み込む
from machine import Pin

ir =  Pin(16, Pin.IN, Pin.PULL_UP)  # GPIO16を入力モードに設定し、プルアップ抵抗を有効化

print(ir.value())  # GPIO16の状態を出力（0または1）