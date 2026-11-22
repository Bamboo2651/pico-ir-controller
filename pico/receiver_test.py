# MicroPython の machine　モジュールからPinという機能を読み込む
from machine import Pin

import time
ir =  Pin(16, Pin.IN, Pin.PULL_UP)  # GPIO16を入力モードに設定し、プルアップ抵抗を有効化

last_value= ir.value()
last_change = time.ticks_us()

durations = []
# 計算処理
while len(durations) < 68:
    current_value = ir.value()  

    if current_value != last_value:
        now = time.ticks_us() #値が変化した時間
        duration = time.ticks_diff(now, last_change) # 前回の変化からの経過時間

        durations.append((last_value, duration)) # 値と経過時間をリストに追加

        last_value = current_value
        last_change = now

# 表示処理
for value, duration in durations:
    print(value, duration)

    bits = []

    for value, duration in durations[4:67:2]:
        if duration < 1000:
            bits.append(0)
        else:
            bits.append(1)
print(bits)

# 1バイトだけのデータを取り出す
# first_byte = 0
# # enumerateを使うことにより、インデックスと要素を同時に取得できる
# for position, bit in enumerate(bits[:8]): 
#     first_byte += bit * (2 ** position) # 2進数を10進数に変換する計算式

# print(hex(first_byte)) # 16進数で表示


# 全バイトを取り出す
decoded_bytes = []
for start in range(0, 32, 8):
    byte_value = 0

    for position, bit in enumerate(bits[start:start + 8]):
        byte_value += bit * (2 ** position)  # 2進数を10進数に変換する計算式

    decoded_bytes.append(byte_value)

for byte_value in decoded_bytes:
    print(hex(byte_value))  # 16進数で表示