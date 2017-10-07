from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
 
  def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        params = parse_qs(urlparse(self.path).query)
        path = urlparse(self.path).path
        self.wfile.write(b"test server")
 
def run():
    server_address = ('localhost', 80)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()

run()
