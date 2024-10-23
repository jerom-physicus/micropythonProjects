import network
import usocket as socket
import machine
import os
import time
import gc
import micropython
# Function to decode URL-encoded data
BOOT_PIN = machine.Pin(0, machine.Pin.IN)
def url_decode(encoded_str):
    # Replace %XX with the corresponding character
    decoded_str = ""
    i = 0
    while i < len(encoded_str):
        if encoded_str[i] == '%' and i + 2 < len(encoded_str):
            # Convert the next two characters to a decimal value and convert to a character
            decoded_str += chr(int(encoded_str[i + 1:i + 3], 16))
            i += 3
        else:
            decoded_str += encoded_str[i]
            i += 1
    return decoded_str

def sleep(delay):
    time.sleep(delay)# Set up an access point
    

output =""
# HTML for the website
html = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Python File Viewer</title>
    <style>
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }

      body,
      html {
        height: 100%;
      }

      body {
        position: relative;
        font-family: monospace;
        margin: 0;
        padding: 0;
        display: flex;
        flex-direction: column;
      }

      h1 {
        padding-top: 15px;
        padding-left: 20px;
        color: aliceblue;
      }

      header {
        display: flex;
        margin-top: 0px;
        background-color: #9650d5;
        height: 60px;
      }

      #file-content {
        width: 100%;
        height: 100%;
        min-height: 200px;
        resize: vertical;
        border-style: solid;
      }

      #shell {
        width: 100%;
        height: 100%;
        overflow-y: scroll;
        border-style: solid;
      }

      input[type="file"] {
        display: block;
        width: 100%;
        margin-left: 20px;
        padding: 3px 16px;
        font-size: 16px;
        cursor: pointer;
        border-radius: 5px;
        border-style: none;
      }
      label {
        background-color: #d4d4d4;
        padding: 7px;
        margin-left: 25px;
        margin-right: 10px;
        border-radius: 5px;
        border-style: groove;
      }

      button {
        display: block;
        margin: 10px;
        margin-left: 30px;
        padding: 8px 16px;
        font-size: 16px;
        cursor: pointer;
        border-radius: 5px;
        border-style: none;
      }
      .container {
        display: flex;
        position: relative;
        width: 60%;
      }
      .line-numbers {
        width: fit-content;
        padding: 12px;
        border-right: 1px solid #ccc;
        user-select: none;
        overflow-y: hidden;
        overflow-x: hidden;
        position: absolute;
        top: 0;
        bottom: 0;
        left: 0;
        font-size: 16px;
      }

      #areas {
        flex: 1; /* Fill remaining space vertically */
        display: flex;
        height: 70%;
        width: 100%;
      }

      textarea {
        width: 100%;
        height: 100%;
        resize: none;
        border-style: solid;
        flex-grow: 1;
        font-size: 16px;
        border: 1px solid #ccc;
        outline: none;
        padding: 10px;
        padding-left: 40px;
      }

      #shell {
        width: 40%;
        height: 100%;
        overflow-y: auto;
        border-style: solid;
      }
      .inputs {
        display: flex;
      }
      #filename {
        width: 15%;
        padding-left: 10px;
      }
      @media only screen and (max-width: 600px) {
        button {
          margin-left: 10px;
        }
        #areas {
          flex-direction: column;
        }
        textarea {
          width: 100%;
          height: 50%;
          resize: horizontal;
          border-style: solid;
          padding: 10px;
          padding-left: 40px;
        }
        .container {
          width: 100%;
          height: 70%;
        }

        #shell {
          width: 100%;
          height: 50%;
          overflow-y: auto;
          border-style: solid;
        }
        #filename {
          width: 50%;
        }
      }
    </style>
  </head>
  <body>
    <header>
      <h1>Qbit 0.1</h1>
      <button id="btn" onclick="handleFile()">Upload</button>
      <button id="runBtn" onclick="runCode()">Run</button>
    </header>
    <div class="inputs">
      <label for="fileInput">Open file</label>
      <input type="file" id="fileInput" style="display: none" />
      <input type="text" id="filename" />
    </div>

    <div id="areas">
      <div class="container">
        <div class="line-numbers" id="lineNumbers"></div>
        <textarea id="file-content"></textarea>
      </div>
      <div id="shell"></div>
    </div>

    <script>
      const lineNumbers = document.getElementById("lineNumbers");
      const codeEditor = document.getElementById("file-content");

      function updateLineNumbers() {
        const lines = codeEditor.value.split(String.fromCharCode(10)).length;


        lineNumbers.innerHTML = "";
        for (let i = 1; i <= lines; i++) {
          lineNumbers.innerHTML += i + "<br>";
        }
      }

      // Function to synchronize scrolling
      function syncScroll() {
        lineNumbers.scrollTop = codeEditor.scrollTop;
      }

      // Add event listeners
      codeEditor.addEventListener("input", updateLineNumbers);
      codeEditor.addEventListener("scroll", syncScroll);

      // Initial setup
      syncScroll();
      setInterval(function () {
        fetch("/data")
          .then((response) => response.text())
          .then((data) => {
            const jsonData = JSON.parse(data);
            data = jsonData.value;
            appendText(data);

            console.log(data);
          })
          .catch((error) => {
            console.error("Error fetching sensor data:", error);
          });
      }, 1000);
      document
        .getElementById("fileInput")
        .addEventListener("input", function () {
          handleFile();
        });
      document.getElementById("btn").addEventListener("click", function () {
        const fileContentDiv = document.getElementById("file-content");
        sendData(fileContentDiv.value);
      });
      function handleFile() {
        const fileInput = document.getElementById("fileInput");
        const file = fileInput.files[0];

        if (file) {
          const reader = new FileReader();
          reader.onload = function (event) {
            let content = event.target.result;
            filenamechange = document.getElementById("filename");
            filenamechange.value = file.name;

            displayContent(content);
          };
          reader.readAsText(file);
        }
      }

      function appendText(data) {
        var textDisplay = document.getElementById("shell");
        var newText = data;
        var newParagraph = document.createElement("p");
        newParagraph.textContent = newText;
        textDisplay.appendChild(newParagraph);

        var container = document.getElementById("shell");
        container.scrollTop = container.scrollHeight;
      }

      function sendData(text) {
        filename = document.getElementById("filename").value;
        const updatedText = text + "String.fromCharCode(10)#<??^" + filename;
        console.log(updatedText);
        var encodedText = encodeURIComponent(updatedText);
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "/send?data=" + encodedText, true);
        xhr.send();
      }

      function displayContent(content) {
        const fileContentDiv = document.getElementById("file-content");
        fileContentDiv.innerHTML = content;
        updateLineNumbers();
      }
      function runCode() {
        var text = "run";
        var encodedText = encodeURIComponent(text);
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "/cmd?data=" + encodedText, true);
        xhr.send();
      }
    </script>
  </body>
</html>

"""
def save_file(filename, content):
    try:
        # Try to remove the existing file
        os.remove(filename)
    except OSError:
        pass  # Ignore if the file doesn't exist

    with open(filename, 'wb') as f:
        f.write(content)
        print("file saved")
        printw("File saved")

        

def run():
    file_name = "index.py"
    try:
        with open(file_name, 'r') as file:
            content = file.read()  # Reads the content of the file
            print("File content:")
            print(content)
            print("Executing file content:")
            exec(content)
    except Exception as e:
        print("Error occurred while reading/execution the file:", e)
        printw(e)
        
def printw(data):
   
    conn, addr = s.accept()
    handle_request(conn,data)    
# Function to handle incoming requests
def handle_request(conn,data):
    global output
    request = conn.recv(1024)
    request = str(request)
    
    # Check if the request is for the root path
    if "GET / " in request:
        conn.send("HTTP/1.1 200 OK\\n")
        conn.send("Content-Type: text/html\\n")
        conn.send("\\n")
        conn.send(html)
    elif '/data' in request: 
        sensor_value = str(data)
        response = '{"value": "' + sensor_value + '"}'
        conn.send('HTTP/1.1 200 OK\\n')
        conn.send('Content-Type: application/json\\n')
        conn.send('Connection: close\\n\\n')
        conn.sendall(response)
        conn.close()# Static string
            
            
        
    # Check if the request is for the "/send" path
    elif "GET /send?" in request:
        data_start = request.find("/send?data=") + len("/send?data=")
        data_end = request.find("HTTP/") - 1
        encoded_data = request[data_start:data_end]
        decoded_data = url_decode(encoded_data)
        print("Received data:", decoded_data)
        output = decoded_data
        save_file("index.py", output)

        conn.send("HTTP/1.1 200 OK\\n")
        conn.send("Content-Type: text/plain\\n")
        conn.send("\\n")
        conn.send("Data received successfully!")
    elif "GET /cmd?" in request:
        data_start = request.find("/cmd?data=") + len("/cmd?data=")
        data_end = request.find("HTTP/") - 1
        encoded_data = request[data_start:data_end]
        decoded_data = url_decode(encoded_data)
        print("Received data:", decoded_data)
        if (decoded_data == "run"):
            run()
 
    else:
        conn.send("HTTP/1.1 404 Not Found\\n")
        conn.send("Content-Type: text/plain\\n")
        conn.send("\\n")
        conn.send("404 Not Found")
    
    conn.close()

# Set up a socket to handle incoming connections
boot_button_pressed = BOOT_PIN.value()
apState = 0


if boot_button_pressed == 0:
    print("Boot button is pressed!")
    apState = 1
time.sleep(2)
def df():
  s = os.statvfs('//')
  return ('{0} MB'.format((s[0]*s[3])/1048576))
if apState:
    ap = network.WLAN(network.AP_IF)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ap.active(True)
    ap.config(essid="ESP32_AP", password="password")      
        
    s.bind(('0.0.0.0', 80))
    s.listen(5)

    print("ESP32 Web Server Started")
    while True:
        data = "connected(^_^)"
        conn, addr = s.accept()
        handle_request(conn,data)

    





