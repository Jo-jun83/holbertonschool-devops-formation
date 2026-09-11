from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 5000
MESSAGE = b"Hello from my first Docker image!\n"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(MESSAGE)


if __name__ == "__main__":
    # "" (empty host) binds to all interfaces, so the server accepts
    # connections from outside the container, not just from localhost inside it.
    server = HTTPServer(("", PORT), Handler)
    print(f"Listening on port {PORT}")
    server.serve_forever()