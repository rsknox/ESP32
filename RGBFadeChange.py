import network
import time

SSID = "801118"
PASSWORD = "rsk366tfw"
BOARD_NAME = "ESP32-White"  # Change to "ESP32-2" on second board

def connect_wifi(ssid, password):
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    if not sta.isconnected():
        print(f"{BOARD_NAME}: Connecting to Wi-Fi...")
        sta.connect(ssid, password)
        timeout = 15  # seconds
        start = time.time()
        while not sta.isconnected():
            if time.time() - start > timeout:
                print(f"{BOARD_NAME}: Could not connect to Wi-Fi")
                return None
            time.sleep(1)
    ip = sta.ifconfig()[0]
    print(f"{BOARD_NAME}: Connected with IP {ip}")
    return ip

if __name__ == "__main__":
    connect_wifi(SSID, PASSWORD)
