import network, espnow

w0 = network.WLAN(network.STA_IF); w0.active(True)
e = espnow.ESPNow(); e.init()
print("ESP-NOW initialized OK")
