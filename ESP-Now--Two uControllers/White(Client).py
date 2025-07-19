import network, socket, time

SSID = "801118"
PASSWORD = "rsk366tfw"
TCP_PORT = 12345
UDP_PORT = 54321

# Connect to Wi-Fi
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect(SSID, PASSWORD)
while not sta.isconnected():
    pass
print("Client connected to Wi-Fi")

def discover_server():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.settimeout(2)
    udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    for _ in range(3):
        udp.sendto(b"DISCOVER_SERVER", ('255.255.255.255', UDP_PORT))

        try:
            msg, addr = udp.recvfrom(1024)
            udp.close()
            print("Server discovered at", msg.decode())
            return msg.decode()
        except OSError:
            pass
    udp.close()
    return None

def connect_to_server():
    while True:
        server_ip = discover_server()
        if server_ip:
            try:
                s = socket.socket()
                s.connect((server_ip, TCP_PORT))
                print("Connected to server")
                return s
            except OSError:
                print("TCP connect failed, retrying...")
        else:
            print("Server not found, retrying...")
        time.sleep(2)

s = connect_to_server()

while True:
    try:
        num = input("Enter number: ")
        s.send(num.encode())
        reply = s.recv(1024)
        print("Reply:", reply.decode())
    except OSError:
        print("Lost connection, reconnecting...")
        s = connect_to_server()
