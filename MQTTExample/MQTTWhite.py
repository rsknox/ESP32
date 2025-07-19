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
TOPIC_PUB = b"%s/feeds/white_to_black" % AIO_USERNAME.encode()
TOPIC_SUB = b"%s/feeds/black_to_white" % AIO_USERNAME.encode()

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASSWORD)
while not wlan.isconnected():
    time.sleep(0.5)
print("Connected to Wi-Fi")

# Handle messages from Black
def sub_callback(topic, msg):
    print("ESP32-White received:", msg.decode())

# Connect to Adafruit IO
client = MQTTClient("ESP32_White", BROKER, user=AIO_USERNAME, password=AIO_KEY, ssl=False)
client.set_callback(sub_callback)
client.connect()
client.subscribe(TOPIC_SUB)
print("Connected to Adafruit IO and subscribed to", TOPIC_SUB.decode())

# Publish numbers periodically
counter = 1
while True:
    message = str(counter)
    client.publish(TOPIC_PUB, message)
    print("ESP32-White sent:", message)

    client.check_msg()  # Check for replies from Black
    counter += 1
    time.sleep(5)
