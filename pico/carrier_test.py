from machine import Pin, PWM
import time

receiver = Pin(16, Pin.IN, Pin.PULL_UP)

carrier = PWM(Pin(15))
carrier.freq(38000)
carrier.duty_u16(21845)

detected = False
start = time.ticks_us()

while time.ticks_diff(time.ticks_us(), start) < 100000:
    if receiver.value() == 0:
        detected = True

carrier.duty_u16(0)

print("赤外線を検出:", detected)