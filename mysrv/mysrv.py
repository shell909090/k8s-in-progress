import os
import http.server
from os import path


# https://docs.python.org/3/library/http.server.html#http.server.BaseHTTPRequestHandler
class ReqHandler(http.server.SimpleHTTPRequestHandler):

    def do_DELETE(self):
        filename = self.path.lstrip('/')
        if not path.isfile(filename):
            self.send_response(404)
            self.end_headers()
            self.wfile.write('file not found'.encode('utf-8'))
            return
        os.remove(filename)
        self.send_response(200)
        self.end_headers()
        self.wfile.write('deleted'.encode('utf-8'))

    def do_POST(self):
        filename = self.path.lstrip('/')
        if path.exists(filename):
            self.send_response(409)
            self.end_headers()
            self.wfile.write('file existed'.encode('utf-8'))
            return
        length = int(self.headers['Content-Length'])
        data = self.rfile.read(length)
        with open(filename, 'wb') as fo:
            fo.write(data)
        self.send_response(201)
        self.end_headers()
        self.wfile.write('saved'.encode('utf-8'))


with http.server.HTTPServer(('', 80), ReqHandler) as httpd:
    httpd.serve_forever()
