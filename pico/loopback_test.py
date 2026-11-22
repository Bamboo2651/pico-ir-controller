from machine import Pin
from ir_tx.nec import NEC
import time


# GP15からPIOを使ってNEC形式の赤外線信号を送信する
transmitter = NEC(Pin(15, Pin.OUT, value=0))

# VS1838BのOUTを接続したGP16で、送信した信号を受け直す
receiver = Pin(16, Pin.IN, Pin.PULL_UP)

received_durations = []
last_value = receiver.value()
last_change = time.ticks_us()


def record_edge(pin):
    """GP16の値が変化するたびに、直前の値と継続時間を記録する。"""
    global last_value, last_change

    now = time.ticks_us()
    duration = time.ticks_diff(now, last_change)
    received_durations.append((last_value, duration))

    last_value = pin.value()
    last_change = now


# 立ち上がりと立ち下がりの両方を記録する
receiver.irq(
    trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING,
    handler=record_edge,
)

# 割り込みを準備してから、点灯信号を1回だけ送る
time.sleep_ms(100)
transmitter.transmit(0x6D82, 0x1F)

while transmitter.busy():
    time.sleep_ms(1)

# 最後の立ち上がりが記録されるまで少し待つ
time.sleep_ms(50)
receiver.irq(handler=None)

print("受信した変化数:", len(received_durations))

for value, duration in received_durations:
    print(value, duration)


# 約9msのリーダーマークを探す。
# 先頭の長い待機時間が毎回異なるため、固定位置にはしない。
leader_index = None

for index, (value, duration) in enumerate(received_durations):
    if value == 0 and 8000 <= duration <= 10000:
        leader_index = index
        break

if leader_index is None:
    print("リーダーマークを検出できませんでした")
else:
    bits = []
    first_space_index = leader_index + 3

    # 各ビットはマークの後の空白時間で0か1かを判断する
    for bit_number in range(32):
        space_index = first_space_index + bit_number * 2

        if space_index >= len(received_durations):
            break

        value, duration = received_durations[space_index]
        bits.append(0 if duration < 1000 else 1)

    print("bits:", bits)

    if len(bits) != 32:
        print("32ビットすべてを受信できませんでした")
    else:
        decoded_bytes = []

        for start in range(0, 32, 8):
            byte_value = 0

            for position, bit in enumerate(bits[start:start + 8]):
                byte_value += bit * (2 ** position)

            decoded_bytes.append(byte_value)

        print("bytes:", [hex(value) for value in decoded_bytes])

        address = decoded_bytes[0] + decoded_bytes[1] * 256
        command = decoded_bytes[2]
        command_inverse = decoded_bytes[3]

        print("address:", hex(address))
        print("command:", hex(command))
        print("command inverse:", hex(command_inverse))

        if command + command_inverse == 0xFF:
            print("Valid command")
        else:
            print("Invalid command")
