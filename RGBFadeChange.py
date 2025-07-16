from machine import Pin, PWM
from time import sleep_ms

# RGB GPIO pins (adjust if needed)
RED_PIN = 14
GREEN_PIN = 12
BLUE_PIN = 27

# PWM frequency
FREQ = 1000

# Initialize PWM for each color (10-bit resolution)
red = PWM(Pin(RED_PIN), freq=FREQ)
green = PWM(Pin(GREEN_PIN), freq=FREQ)
blue = PWM(Pin(BLUE_PIN), freq=FREQ)

# Max PWM duty for ESP32
MAX_DUTY = 1023


def set_color(r, g, b):
    # Convert 0–255 to 0–1023 for PWM
    red.duty(int(r * 1023 / 255))
    green.duty(int(g * 1023 / 255))
    blue.duty(int(b * 1023 / 255))


def loop():
    step = 5
    delay = 20

    # 1. RED ↑ (0 → 255)
    for r in range(0, 256, step):
        set_color(r, 0, 0)
        sleep_ms(delay)

    # 2. RED ↓ (255 → 0), GREEN ↑ (0 → 255)
    for g in range(0, 256, step):
        r = 255 - g
        set_color(r, g, 0)
        sleep_ms(delay)

    # 3. GREEN ↓ (255 → 0), BLUE ↑ (0 → 255)
    for b in range(0, 256, step):
        g = 255 - b
        set_color(0, g, b)
        sleep_ms(delay)

    # 4. BLUE ↓ (255 → 0), RED ↑ (0 → 255)
    for r in range(0, 256, step):
        b = 255 - r
        set_color(r, 0, b)
        sleep_ms(delay)


# Main loop
while True:
    loop()
