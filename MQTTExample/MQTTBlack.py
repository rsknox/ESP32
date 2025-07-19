import network
import time
from umqtt.simple import MQTTClient

# Wi-Fi credentials
WIFI_SSID = "801118"
WIFI_PASSWORD = "rsk366tfw"

# Adafruit IO credentials
AIO_USERNAME = "rsknox"
AIO_KEY = "aio_bKRF21rigyvTvD2xnCVwdNZQFLtx"
BROKER = "io.adafruit.com"

# Topics
TOPIC_SUB = b"%s/feeds/white_to_black" % AIO_USERNAME.encode()
TOPIC_PUB = b"%s/feeds/black_to_white" % AIO_USERNAME.encode()

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASSWORD)
while not wlan.isconnected():
    time.sleep(0.5)
print("Connected to Wi-Fi")

# Handle messages from White
def sub_callback(topic, msg):
    num = int(msg.decode())
    num += 1  # Add one to the received number
    print("ESP32-Black received:", num - 1, "sending back:", num)
    client.publish(TOPIC_PUB, str(num))

# Connect to Adafruit IO
client = MQTTClient("ESP32_Black", BROKER, user=AIO_USERNAME, password=AIO_KEY, ssl=False)
client.set_callback(sub_callback)
client.connect()
client.subscribe(TOPIC_SUB)
print("Connected to Adafruit IO and subscribed to", TOPIC_SUB.decode())

# Keep listening for messages
while True:
    client.check_msg()  # Non-blocking
    time.sleep(0.1)
