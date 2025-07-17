import network
import socket
from machine import Pin, PWM
try:
    from ure import unquote  # Some MicroPython builds have this
except ImportError:
    import ubinascii
    def unquote(s):
        res = s.replace('+', ' ')
        parts = res.split('%')
        out = parts[0]
        for part in parts[1:]:
            if len(part) >= 2:
                hex_val = part[:2]
                rest = part[2:]
                out += chr(int(hex_val, 16)) + rest
            else:
                out += '%' + part
        return out


# === Pins for common anode RGB LED ===
red_pwm = PWM(Pin(14), freq=1000)
green_pwm = PWM(Pin(12), freq=1000)
blue_pwm = PWM(Pin(27), freq=1000)

# === Initial brightness (0-1023, but inverted for common anode) ===
brightness = {'red': 1023, 'green': 1023, 'blue': 1023}

# === Update LED brightness ===
def update_pwm():
    red_pwm.duty(brightness['red'])
    green_pwm.duty(brightness['green'])
    blue_pwm.duty(brightness['blue'])

# === Wi-Fi connection ===
SSID = '801118'
PASSWORD = 'rsk366tfw'

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(SSID, PASSWORD)

while not station.isconnected():
    pass

ip = station.ifconfig()[0]
print("Connected. Open this IP in your browser:", ip)

# === Generate HTML page with sliders ===
def generate_html():
    html = """<!DOCTYPE html>
    <html>
    <head>
        <title>RGB LED PWM Control</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: sans-serif; text-align: center; }}
            input[type=range] {{ width: 80%%; }}
            label {{ display: block; margin-top: 20px; font-size: 20px; }}
        </style>
    </head>
    <body>
        <h2>ESP32 RGB LED Control</h2>
        <form action="/" method="get">
            <label>Red: {rval}</label>
            <input type="range" min="0" max="1023" name="red" value="{rval}" onchange="this.form.submit()">
            <label>Green: {gval}</label>
            <input type="range" min="0" max="1023" name="green" value="{gval}" onchange="this.form.submit()">
            <label>Blue: {bval}</label>
            <input type="range" min="0" max="1023" name="blue" value="{bval}" onchange="this.form.submit()">
        </form>
    </body>
    </html>
    """.format(rval=1023 - brightness['red'],
               gval=1023 - brightness['green'],
               bval=1023 - brightness['blue'])
    return html



# === Web server ===
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
server = socket.socket()
server.bind(addr)
server.listen(1)
print("Server listening on", addr)

while True:
    client, addr = server.accept()
    print("Client connected from", addr)
    request = client.recv(1024).decode()
    print("Request:", request)

    try:
        # === Parse GET parameters ===
        if "GET /?" in request:
            params = request.split('GET /?')[1].split(' ')[0]
            for pair in params.split('&'):
                if '=' in pair:
                    key, value = pair.split('=')
                    key = unquote(key)
                    value = int(unquote(value))
                    if key in brightness:
                        # Invert PWM value for common anode
                        brightness[key] = 1023 - min(max(value, 0), 1023)
                        print(f"{key} set to {value}")
        update_pwm()
    except Exception as e:
        print("Error parsing request:", e)

    response = generate_html()
    client.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
    client.sendall(response)
    client.close()
