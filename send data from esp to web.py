import network
import usocket as socket
import machine
import ujson

# Replace these with your WiFi credentials
ssid = "YourSSID"
password = "YourPassword"

# Replace this with the pin where your sensor is connected
sensor_pin = 34

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password)

html = """<!DOCTYPE html>
<html>
<head><title>ESP32 Sensor Data</title></head>
<body>
  <h1>Sensor Data</h1>
  <p id="sensorData">---</p>
  <form id="inputForm">
    <label for="inputValue">Enter Value:</label>
    <input type="text" id="inputValue" name="inputValue" />
    <button type="button" onclick="sendInputValue()">Send</button>
  </form>
  <form action="/upload" method="post" enctype="multipart/form-data">
    <input type="file" name="file" accept=".py">
    <input type="submit" value="Upload">
</form>
  <script>
    setInterval(function() {
      fetch('/data')
        .then(response => response.text())
        .then(data => {
          const jsonData = JSON.parse(data);
          document.getElementById('sensorData').innerText = jsonData.value;
        })
        .catch(error => {
          console.error('Error fetching sensor data:', error);
        });
    }, 1000);

    function sendInputValue() {
      const inputValue = document.getElementById('inputValue').value;
      fetch('/sendInput', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ value: inputValue }),
      })
      .then(response => console.log('Input value sent successfully'))
      .catch(error => console.error('Error sending input value:', error));
    }
  </script>
</body>
</html>
"""

def serve_webpage(conn):
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(html)
    conn.close()

def serve_sensor_data(conn):
    sensor_value = "hello"  # Static string
    response = '{"value": "' + sensor_value + '"}'
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: application/json\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()

def handle_input_value(conn, data):
  
        print(data)
        content_length = len(data)
        json_data = ujson.loads(data.decode("utf-8"))
        input_value = json_data.get('value', '')
        print('Received input value:', input_value)
    

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

adc = machine.ADC(sensor_pin)

while True:
    conn, addr = s.accept()
    request = conn.recv(1024)
    request_str = str(request)

    if '/data' in request_str:
        serve_sensor_data(conn)
    elif '/sendInput' in request_str:
        double_linebreak = request_str.find('\r\n\r\n')
        if double_linebreak != -1:
            input_data = request[double_linebreak+4:]
            print(input_data)
            handle_input_value(conn, input_data)
        else:
            conn.send('HTTP/1.1 400 Bad Request\n')
            conn.send('Connection: close\n\n')
    else:
        serve_webpage(conn)
