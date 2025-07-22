from machine import Pin, Timer

# Define RGB pins (common anode, so HIGH = off, LOW = on)
red = Pin(14, Pin.OUT, value=1)
green = Pin(12, Pin.OUT, value=1)
blue = Pin(27, Pin.OUT, value=1)

# Callback functions for each color
def toggle_red(timer):
    red.value(not red.value())  # Toggle red channel

def toggle_green(timer):
    green.value(not green.value())  # Toggle green channel

def toggle_blue(timer):
    blue.value(not blue.value())  # Toggle blue channel

# Create hardware timers
tim_red = Timer(0)
tim_green = Timer(1)
tim_blue = Timer(2)

# Configure timers for different blink intervals (ms)
tim_red.init(period=1000, mode=Timer.PERIODIC, callback=toggle_red)
tim_green.init(period=200, mode=Timer.PERIODIC, callback=toggle_green)
tim_blue.init(period=250, mode=Timer.PERIODIC, callback=toggle_blue)

# Main loop does nothing; LEDs blink independently
while True:
    pass
