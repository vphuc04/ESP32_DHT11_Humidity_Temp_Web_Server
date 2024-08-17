import socket
import dht
import machine

# DHT sensor setup
dht_pin = dht.DHT11(machine.Pin(4))  # Đảm bảo rằng bạn đã thiết lập đúng chân GPIO

def read_dht():
    global temp, hum
    temp = hum = 0
    try:
        dht_pin.measure()
        temp = dht_pin.temperature()
        hum = dht_pin.humidity()
        if (isinstance(temp, float) and isinstance(hum, float)) or (isinstance(temp, int) and isinstance(hum, int)):
            msg = (b'{0:3.1f},{1:3.1f}'.format(temp, hum))
            print("Temperature: ", temp)
            print("Humidity: ", hum)
            hum = round(hum, 2)
            return temp, hum
        else:
            print("Invalid sensor readings.")
            return None, None
    except OSError as e:
        print("Error reading sensor:", e)
        return None, None

def web_page(temp, hum):
    html = """<html><head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta charset="UTF-8">
    <style>
        body {
            padding: 20px;
            margin: auto;
            width: 50%;
            text-align: center;
            font-family: Arial, Helvetica, sans-serif;
        }
        #logo {
            width: 50%; /* Thay đổi kích thước logo */
            margin-bottom: 20px;
        }
        .progress { background-color: #F5F5F5; }
        .progress.vertical {
            position: relative;
            width: 25%;
            height: 60%;
            display: inline-block;
            margin: 20px;
        }
        .progress.vertical > .progress-bar {
            width: 100% !important;
            position: absolute;bottom: 0;
        }
        .progress-bar { background: linear-gradient(to top, hsl(352, 51%, 62%) 0%, #f12711 100%); }
        .progress-bar-hum { background: linear-gradient(to top, #9CECFB 0%, hsl(256, 100%, 51%) 50%, hsl(217, 94%, 20%) 100%); }
        .progress-bar-temp { background: linear-gradient(to top, #9CECFB 0%, hsl(256, 100%, 51%) 50%, hsl(217, 94%, 20%) 100%); }
        p {
            position: absolute;
            font-size: 1.5rem;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 5;
        }
    </style>
    <script>
        function updateData() {
            var xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4 && xhr.status == 200) {
                    var data = JSON.parse(xhr.responseText);
                    document.getElementById("temp").innerText = data.temperature + "°C";
                    document.getElementById("humidity").innerText = data.humidity + "%";
                    document.getElementById("temp-bar").style.height = data.temperature + "%";
                    document.getElementById("humidity-bar").style.height = data.humidity + "%";
                }
            };
            xhr.open("GET", "/data", true);
            xhr.send();
        }

        setInterval(updateData, 1000);  // Cập nhật mỗi 1 giây
    </script>
    </head><body>
        <img id="logo" src="https://file1.hutech.edu.vn/file/editor/homepage/stories/hinh34/logo%20CMYK-01.png" alt="HUTECH Logo">
        <h1>MicroPython và ESP32: Web server giám sát nhiệt độ và độ ẩm</h1>
        <div class="progress vertical">
            <p id="temp">"""+str(temp)+"""&deg;C<p>
            <div id="temp-bar" role="progressbar" style="height: """+str(temp)+"""%;" class="progress-bar progress-bar-temp"></div>
        </div>
        <div class="progress vertical">
            <p id="humidity">"""+str(hum)+"""%</p>
            <div id="humidity-bar" role="progressbar" style="height: """+str(hum)+"""%;" class="progress-bar progress-bar-hum"></div>
        </div>
    </body></html>"""
    return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    print('Content = %s' % str(request))
    if b'/data' in request:
        temp, hum = read_dht()
        response = '{"temperature": '+str(temp)+', "humidity": '+str(hum)+'}'
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: application/json\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
    else:
        temp, hum = read_dht()
        response = web_page(temp, hum)
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
    conn.close()



