from machine import Pin, PWM
import time

carrier = PWM(Pin(15))
carrier.freq(38000)
carrier.duty_u16(0)

def mark(duration_us):
    carrier.duty_u16(21845)
    time.sleep_us(duration_us)
    carrier.duty_u16(0)


def space(duration_us):
    time.sleep_us(duration_us)


def send_bit(bit):
    mark(560)

    if bit == 0:
        space(560)
    else:
        space(1690)

def send_byte(byte_value):
    for position in range(8):
        bit = (byte_value >> position) & 1
        send_bit(bit)


ADDRESS_LOW = 0x82
ADDRESS_HIGH = 0x6D


def send_nec(command):
    mark(9000)
    space(4500)

    send_byte(ADDRESS_LOW)
    send_byte(ADDRESS_HIGH)
    send_byte(command)
    send_byte(0xFF - command)

    mark(560)

while True:
    send_nec(0x1E)
    print("消灯信号を送信しました")
    time.sleep(1)
