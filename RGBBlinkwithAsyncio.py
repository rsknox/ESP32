import uasyncio as asyncio
from machine import Pin

# Define RGB pins (common anode, so HIGH = off, LOW = on)
red = Pin(14, Pin.OUT, value=1)
green = Pin(12, Pin.OUT, value=1)
blue = Pin(27, Pin.OUT, value=1)

async def blink(pin, period_ms):
    while True:
        pin.value(not pin.value())  # Toggle LED
        await asyncio.sleep_ms(period_ms)

async def main():
    # Create three independent blinking tasks
    asyncio.create_task(blink(red, 500))   # Red: 1 second
    asyncio.create_task(blink(green, 300))  # Green: 200 ms
    asyncio.create_task(blink(blue, 100))   # Blue: 250 ms
    
    # Keep the main loop alive
    while True:
        await asyncio.sleep(1)

# Run the event loop
asyncio.run(main())
