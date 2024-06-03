# Script to progressively blink between leds on pins 2 and 4 with incrementing time delays on each loop
import machine
import time
led = machine.Pin(4, machine.Pin.OUT)
led2 = machine.Pin(2, machine.Pin.OUT)
d1 = 0
d2 = 0
for i in range(10):
    d1 = 1.0 - 0.1 * i
    d2 = 1.0 - d1
    led.value(1)
    led2.value(0)
    time.sleep(d1)
    led.value(0)
    led2.value(1)
    time.sleep(d2)

