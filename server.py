import os
import http.server
import socketserver
from urllib import parse

from http import HTTPStatus

VERIFY_TOKEN = "a1993ff202a0f1b4ffae"

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        
        query = parse.urlparse(self.path).query
        path = parse.urlparse(self.path).path
        query_components = dict(qc.split("=") for qc in query.split("&"))

        if path == "/verification":
            mode = query_components['hub.mode']
            token = query_components['hub.verify_token']
            challenge = query_components['hub.challenge']

            if mode is not None and token is not None:
                if (mode == 'subscribe') and (token == VERIFY_TOKEN): 
                    print('WEBHOOK_VERIFIED')
                    self.send_response(HTTPStatus.OK)
                    self.end_headers()
                    msg = challenge
                    self.wfile.write(msg.encode())
                else:
                    self.send_response(HTTPStatus.FORBIDDEN)
                    self.end_headers()   
        

port = int(os.getenv('PORT', 80))
print('Listening on port %s' % (port))
httpd = socketserver.TCPServer(('', port), Handler)
httpd.serve_forever()
