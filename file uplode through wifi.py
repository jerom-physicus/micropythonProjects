import network
import usocket as socket
import ure
import os

ssid = "T E S L A 4g"
password = "87654321"

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password)

HTML = """<!DOCTYPE html>
<html>
<head><title>ESP32 File Upload</title></head>
<body>
<h2>Upload a file</h2>
<form action="/upload" method="post" enctype="multipart/form-data">
    <input type="file" name="file" accept=".py">
    <input type="submit" value="Upload">
</form>
</body>
</html>
"""

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('192.168.4.1', 80))
s.listen(5)

def parse_request(request):
    boundary_start = request.find(b'boundary=')
    if boundary_start == -1:
        return None, None

    boundary_end = request.find(b'\r\n', boundary_start)
    if boundary_end == -1:
        return None, None

    boundary = request[boundary_start + 9:boundary_end]

    parts = request.split(boundary)

    # Skip the first and last parts as they don't contain file data
    for part in parts[1:-1]:
        header, content = part.split(b'\r\n\r\n', 1)
        filename_match = ure.search(rb'filename="(.+)"', header)
        if filename_match:
            filename = filename_match.group(1).decode('utf-8')
            return filename, content.replace(b'\r\n--', b'')  # Remove trailing CRLF and boundary

    return None, None

def save_file(filename, content):
    try:
        # Try to remove the existing file
        os.remove(filename)
    except OSError:
        pass  # Ignore if the file doesn't exist

    with open(filename, 'wb') as f:
        f.write(content)

while True:
    conn, addr = s.accept()
    request = conn.recv(4096)
    conn.sendall("HTTP/1.1 200 OK\n")
    conn.sendall("Content-Type: text/html\n")
    conn.sendall("Connection: close\n\n")

    if b"POST /upload" in request:
        filename, content = parse_request(request)
        if filename and content:
            save_file(filename, content)

    conn.sendall(HTML)
    conn.close()
