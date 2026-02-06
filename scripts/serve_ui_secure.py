#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class SecureHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Basic security headers for static UI
        self.send_header('Content-Security-Policy', "default-src 'self'; style-src 'self' 'unsafe-inline';")
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('Referrer-Policy', 'no-referrer')
        super().end_headers()

    def translate_path(self, path):
        # Serve from ./frontend directory
        root = os.path.join(os.getcwd(), 'frontend')
        return super().translate_path(path if path != '/' else '/index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', '8080'))
    server = HTTPServer(('0.0.0.0', port), SecureHandler)
    print(f"Serving secure UI at http://localhost:{port}")
    server.serve_forever()
