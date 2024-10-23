import network
import socket
from machine import Pin
from neopixel import NeoPixel

# Set up NeoPixel
np_pin = Pin(45, Pin.OUT)  # Pin where your NeoPixel is connected
np = NeoPixel(np_pin, 1)  # 1 NeoPixel LED

# Set up ESP32 in Access Point (AP) mode
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='ESP32-Color-Picker', authmode=network.AUTH_OPEN)

# Web server HTML for the RGB color picker
html = """<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ESP32 NeoPixel Color Picker</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            text-align: center;
            background-color: #f4f4f9;
        }
        h1 {
            color: #333;
        }
        input[type="color"] {
            width: 80%;
            height: 50px;
            border: none;
            margin-bottom: 20px;
        }
        button {
            width: 80%;
            padding: 15px;
            font-size: 18px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <h1>Choose a Color</h1>
    <input type="color" id="colorPicker" name="color" value="#ff0000">
    <button onclick="sendColor()">Set Color</button>
    <script>
        function sendColor() {
            let color = document.getElementById('colorPicker').value;
            let xhr = new XMLHttpRequest();
            xhr.open("GET", "/color?rgb=" + color.substring(1), true);
            xhr.send();
        }
    </script>
</body>
</html>
"""

# Function to handle incoming HTTP requests
def web_page():
    return html

# Start web server
def serve():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    print('Listening on', addr)

    while True:
        cl, addr = s.accept()
        print('Client connected from', addr)
        request = cl.recv(1024)
        request = str(request)

        if "/color?rgb=" in request:
            color = request.split("/color?rgb=")[1].split(' ')[0]
            red = int(color[0:2], 16)
            green = int(color[2:4], 16)
            blue = int(color[4:6], 16)
            np[0] = (red, green, blue)
            np.write()

        response = web_page()
        cl.send('HTTP/1.1 200 OK\r\n')  # Corrected the header format
        cl.send('Content-Type: text/html\r\n')
        cl.send('Connection: close\r\n\r\n')  # Correctly close the headers
        cl.sendall(response)  # Send the HTML content
        cl.close()

# Run the server
serve()

