import network
import usocket as socket
import urequests
import ujson

# Set up the ESP32 as an access point
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="ESP32-Access-Point", password="password")

# Set up a simple web server
def web_page():
    html = """<!DOCTYPE html>
    <html>
        <head>
            <title>ESP32 Web Server</title>
            <script>
                function submitForm() {
                    var input_data = document.getElementById("input_data").value;
                    var xhr = new XMLHttpRequest();
                    xhr.open("POST", "/", true);
                    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
                    xhr.send("input_data=" + input_data);
                }
            </script>
        </head>
        <body>
            <h1>ESP32 Web Server</h1>
            <form onsubmit="submitForm(); return false;">
                <label for="input_data">Enter text:</label>
                <input type="text" id="input_data" name="input_data">
                <input type="submit" value="Submit">
            </form>
        </body>
    </html>
    """
    return html

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = str(request)

    input_data = None

    # Extract input data from the request
    if "input_data" in request:
        input_data = request.split("input_data=")[1].split("&")[0]

    # Print the input data
    if input_data:
        print("Input data:", input_data)

        # Send the input data to another device (e.g., ESP32)
        # Replace the URL with your destination endpoint
        destination_url = "http://192.168.4.1/"

        try:
            # Encode the dictionary into a bytes-like object
            data_to_send = ujson.dumps({'input_data': input_data})
            response = urequests.post(destination_url, data=data_to_send)
            print("Server Response:", response.text)
            response.close()
        except Exception as e:
            print("Error sending data:", e)

    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
