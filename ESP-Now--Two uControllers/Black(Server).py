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
ip = sta.ifconfig()[0]
print("Server IP:", ip)

# UDP responder for discovery
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(('', UDP_PORT))
udp.setblocking(False)

# TCP server socket
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp.bind(('', TCP_PORT))
tcp.listen(1)
tcp.settimeout(1)

print("Server ready")

while True:
    # Respond to discovery pings
    try:
        msg, addr = udp.recvfrom(1024)
        if msg == b"DISCOVER_SERVER":
            udp.sendto(ip.encode(), addr)
    except OSError:
        pass

    # Accept new TCP connection
    try:
        conn, addr = tcp.accept()
        print("Client connected from", addr)
        conn.settimeout(25)
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    print("Client disconnected")
                    break
                try:
                    number = int(data.decode())
                    print("Received:", number)
                    conn.send(str(number + 1).encode())
                except:
                    conn.send(b"ERR")
            except OSError:
                # Connection timeout or drop
                print("Connection lost")
                break
    except OSError:
        pass
