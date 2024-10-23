import network
import socket
from machine import Pin

# Motor driver pins
in1 = Pin(41, Pin.OUT)
in2 = Pin(42, Pin.OUT)
in3 = Pin(2, Pin.OUT)
in4 = Pin(1, Pin.OUT)

# Initialize motors to stop
in1.off()
in2.off()
in3.off()
in4.off()

# Set up ESP32 as an Access Point
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='ESP32-Robot', password='12345678')

# Web page with simple directional controls
def web_page():
    html = """<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <style>
      body {
        font-family:monospace;
        text-align: center;
        background-color: #050505;
      }
      h1 {
        
        color: #eeeeee;
      }
      i{
        font-family:monospace;

      }
      div {
        display: inline-block;
        background-color: #d9d9d9;
        width: fit-content;
        height: fit-content;
        border-radius: 50%;
        margin: 5px;
      }
      .icon-button {
       font-weight: 1000;
        display: inline-block;
        font-size: 24px;
        padding: 25px 30px 25px 30px;
        cursor: pointer;
        text-align: center;
        text-decoration: none;
        outline: none;
        color: rgb(127, 65, 251);
        user-select: none;
      }
      .stop-btn {
        display: inline-block;
        font-size: 20px;
        padding: 35px 30px 35px 30px;
        cursor: pointer;
        margin: 10px;
        text-align: center;
        text-decoration: none;
        outline: none;
        color: rgb(127, 65, 251);
        user-select: none;
      }
    </style>
  </head>
  <body>
    <h1>Atom S3 Car Control</h1>
    <div>
        <a id="tag" class="icon-button" href="/forward"
          >F</a>
    </div>
      <p>
        <div>
            <a class="icon-button" href="/left"
              
            >L</a>
        </div>
        <div>
          <a class="stop-btn" href="/stop">Stop</a>
        </div>
        <div>

          <a class="icon-button" href="/right"
          >R</a>
        </div>
      </p>

    <div>
      <a class="icon-button" href="/backward">B</a>
        </div>
  </body>
</html>
"""
    return html

# Function to control motors based on path
def control_motors(path):
    if path == '/forward':
        in1.on()
        in2.off()
        in3.on()
        in4.off()
    elif path == '/backward':
        in1.off()
        in2.on()
        in3.off()
        in4.on()
    elif path == '/left':
        in1.off()
        in2.on()
        in3.on()
        in4.off()
    elif path == '/right':
        in1.on()
        in2.off()
        in3.off()
        in4.on()
    elif path == '/stop':
        in1.off()
        in2.off()
        in3.off()
        in4.off()

# Create socket for web server
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print("ESP32 is running as an Access Point, connect to: 'ESP32-Robot'")

# Listen for connections
while True:
    conn, addr = s.accept()
    print('Got connection from', addr)
    request = conn.recv(1024)
    request = str(request)
    print('Content = %s' % request)
    
    # Extract the path from the request
    path = None
    if 'GET /forward' in request:
        path = '/forward'
    elif 'GET /backward' in request:
        path = '/backward'
    elif 'GET /left' in request:
        path = '/left'
    elif 'GET /right' in request:
        path = '/right'
    elif 'GET /stop' in request:
        path = '/stop'
    
    # Control motors based on the path
    if path:
        control_motors(path)
    
    # Send response back to the browser
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()

