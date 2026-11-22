from machine import Pin
from ir_tx.nec import NEC
import time

nec = NEC(Pin(15, Pin.OUT, value=0))

nec.transmit(0x6D82, 0x1F)

while nec.busy():
    time.sleep_ms(1)

print("点灯信号を送信しました")