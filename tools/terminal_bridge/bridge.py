from __future__ import annotations
import json, os, platform, secrets, subprocess, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

HOST = "127.0.0.1"
PORT = int(os.getenv("AVE_BRIDGE_PORT", "8765"))
TOKEN = os.getenv("AVE_BRIDGE_TOKEN")
TIMEOUT = int(os.getenv("AVE_BRIDGE_TIMEOUT", "20"))

if not TOKEN:
    raise SystemExit("Set AVE_BRIDGE_TOKEN before starting the bridge.")


def run(argv, timeout=TIMEOUT):
    p = subprocess.run(argv, capture_output=True, text=True, timeout=timeout, shell=False)
    return {"ok": p.returncode == 0, "code": p.returncode, "stdout": p.stdout[-20000:], "stderr": p.stderr[-10000:]}


def adb(args):
    return run(["adb", *args])


def frida(args):
    return run(["frida", *args])


def emulator(args):
    return run(["emulator", *args])


def json_out(handler, code, obj):
    raw = json.dumps(obj, ensure_ascii=False).encode("utf-8")
    handler.send_response(code)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(raw)))
    handler.end_headers()
    handler.wfile.write(raw)


class Handler(BaseHTTPRequestHandler):
    server_version = "AVEBridge/1.0"

    def log_message(self, fmt, *args):
        print("[AVEBridge] " + fmt % args)

    def auth(self):
        supplied = self.headers.get("X-AVE-Token", "")
        return secrets.compare_digest(supplied, TOKEN)

    def do_GET(self):
        if not self.auth():
            return json_out(self, 401, {"ok": False, "error": "unauthorized"})
        q = parse_qs(urlparse(self.path).query)
        path = urlparse(self.path).path
        if path == "/health":
            return json_out(self, 200, {"ok": True, "service": "ave-bridge", "version": "1.0", "time": time.time()})
        if path == "/system":
            return json_out(self, 200, {"ok": True, "platform": platform.platform(), "python": platform.python_version()})
        if path == "/adb/devices":
            return json_out(self, 200, adb(["devices", "-l"]))
        if path == "/adb/packages":
            return json_out(self, 200, adb(["shell", "pm", "list", "packages"]))
        if path == "/adb/prop":
            name = q.get("name", [""])[0]
            if not name or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._:-" for c in name):
                return json_out(self, 400, {"ok": False, "error": "invalid property name"})
            return json_out(self, 200, adb(["shell", "getprop", name]))
        if path == "/emulator/avds":
            return json_out(self, 200, emulator(["-list-avds"]))
        if path == "/frida/processes":
            return json_out(self, 200, frida(["ps", "-U"]))
        if path == "/frida/devices":
            return json_out(self, 200, frida(["ls-devices"]))
        return json_out(self, 404, {"ok": False, "error": "not found"})

    def do_POST(self):
        if not self.auth():
            return json_out(self, 401, {"ok": False, "error": "unauthorized"})
        path = urlparse(self.path).path
        n = int(self.headers.get("Content-Length", "0"))
        try:
            body = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            return json_out(self, 400, {"ok": False, "error": "invalid json"})
        if path == "/emulator/start":
            name = body.get("avd", "")
            if not isinstance(name, str) or not name or len(name) > 100 or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-" for c in name):
                return json_out(self, 400, {"ok": False, "error": "invalid avd name"})
            p = subprocess.Popen(["emulator", "-avd", name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return json_out(self, 202, {"ok": True, "pid": p.pid, "avd": name})
        if path == "/emulator/stop":
            serial = body.get("serial", "")
            if not isinstance(serial, str) or not serial.startswith("emulator-") or not serial[9:].isdigit():
                return json_out(self, 400, {"ok": False, "error": "invalid emulator serial"})
            return json_out(self, 200, adb(["-s", serial, "emu", "kill"]))
        return json_out(self, 404, {"ok": False, "error": "not found"})


if __name__ == "__main__":
    print(f"AVE Bridge listening on http://{HOST}:{PORT}")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
