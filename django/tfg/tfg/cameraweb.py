import picamera
from datetime import datetime
import io
import logging
import socketserver
from threading import Condition
from http import server
from time import sleep

PAGE="""\
<html>
<head>
<title>Raspberry Pi - Surveillance Camera</title>
</head>
<body>
<center><h1>Raspberry Pi - Surveillance Camera</h1></center>
<center><a href="/shot.html"><img src="stream.mjpg" width="640" height="480"></a></center>
</body>
</html>
"""
Redirection="""<html><head><meta http-equiv="refresh" content="0;URL=/index.html"></head></html>"""

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()
        self.camera=picamera.PiCamera(resolution='640x480', framerate=24)
        self.camera.vflip=True

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)
    def shot_camera(self):
        self.camera.wait_recording(1)
        self.camera.stop_recording()
        sleep(1)
        self.camera.resolution=(1920,1080)
        self.camera.start_preview()
        sleep(5)
        self.camera.capture("/home/pi/tfg/talvez" + datetime.now().strftime("%d-%b-%Y.(%H_%M_%S_%f)") + ".jpg")
        self.camera.resolution=(640,480)
        self.camera.start_recording(self, format='mjpeg')
    def start_recording(self):
        #Uncomment the next line to change your Pi's Camera rotation (in degrees)
        #camera.rotation = 90
        self.camera.start_recording(self, format='mjpeg')
    def stop_camera(self):
        self.camera.stop_recording()

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        elif self.path == '/shot.html':
            output.shot_camera()
            content = Redirection.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

output = StreamingOutput()
output.start_recording()

address = ('192.168.10.86', 8000)
serveur = StreamingServer(address, StreamingHandler)
serveur.serve_forever()

