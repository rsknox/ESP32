import network
import ubinascii

# Create a WLAN object in station mode
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Get the MAC address (as bytes) and convert to a readable string
mac_bytes = wlan.config('mac')
mac_address = ubinascii.hexlify(mac_bytes, ':').decode().upper()

print("ESP32 MAC Address:", mac_address)
