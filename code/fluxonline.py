# Source code from the official PiCamera package
# http://picamera.readthedocs.io/en/latest/recipes2.html#web-streaming

from cgi import print_form
import io
import socket
import cv2
import picamera
import logging
import socketserver
from threading import Condition
from http import server

from color_analysis import LoadHistogramsAllFromReferencesBird, tellClosestBird
from enregistrement_resize import enregistre, resize
from mask import create_mask


from mask import create_mask
def getSurfaceOfImage(img):
    flattened = [val for pix in img for val in pix]
    return flattened.count(255)

# renvoie image avec le plus de pixel blanc
def setOptimalPhoto():
    global img_opti, score
    img_opti = img_list[score.index(max(score))]
    





PAGE="""\
<html>
<head>
<title>Raspberry Pi - Cabane a oiseaux</title>
</head>
<body>
<center><h1>Raspberry Pi - Cabane a oiseaux</h1></center>
<center><img src="stream.mjpg" width="640" height="480"></center>
</body>
</html>
"""

class StreamingOutput(object):
    c=0
    framefond=[]
    compteur = 0
    img_list = []
    score = []
    prev = 0
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            print("frame")
            if(c==0):
                print("ici1")
                framefond=cv2.resize(self.frame,(800, 548))
                c+=1
            if(c!=0):
                print("ici2")
                frame=cv2.resize(self.frame,(800, 548))
                mask=create_mask(frame,framefond,50)
                surface = getSurfaceOfImage(mask)
                if surface > 100 and compteur < 5:
                    score.append(surface)
                    img_list.append(frame)
                    compteur += 1
                    print("ici")
                elif compteur == 5:
                    print("enfin ...")
                    setOptimalPhoto()
        
                    histoRefs = LoadHistogramsAllFromReferencesBird()
                    img_opti = cv2.resize(img_opti,(800, 548))
                    #appel comparaison
                    tellClosestBird(img_opti, histoRefs)
        
                    img_list = []
                    score = []
                    compteur = 0
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

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
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

with picamera.PiCamera(resolution='540x480', framerate=24) as camera:
    print("he")
    output = StreamingOutput()
    #Uncomment the next line to change your Pi's Camera rotation (in degrees)
    #camera.rotation = 90
    camera.start_recording(output, format='mjpeg')
    
    try:
        while True:
            print("bouh")
            address = ('', 8000)
            server = StreamingServer(address, StreamingHandler)
            server.serve_forever()
    finally:
        camera.stop_recording()

