import http.server
from http.server import BaseHTTPRequestHandler, HTTPServer
from re import template
from urllib.parse import urlparse
import logging
import json
import algo
import pdb

logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RequestHandler(BaseHTTPRequestHandler):
    HTML_HEADERS = {
        "Content-type": "text/html",
    }

    def get_template(self, path:str) -> bytes:
        """
        reads file in path and returns bytes string
        which has been cleaned
        """
        with open(path, "rb") as file:
            data = file.read()
        return data.replace(b"\n",b"").replace(b"\t", b"") 

    def send_template(self, content):
        self.send_response(200)
        for i in self.HTML_HEADERS.items():
            self.send_header(i[0], i[1])
        self.send_header("Content-length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        logger.info("GET request")
        path = urlparse(self.path)
        if path.path == "/":
            template_bytes = self.get_template("./src/index.html")
            self.send_template(template_bytes)

    def do_POST(self):
        logger.info("POST request")
        path = urlparse(self.path)
        if path.path == "/":
            length = int(self.headers.get("content-length"))
            field_data = self.rfile.read(length)
            json_data = json.loads(field_data)
            split_data = algo.split_box(json_data)
            logger.info("posted data: %s %s", json_data, split_data)

            data = (json.dumps(split_data)).encode()
            self.send_response(200)
            self.send_header("Content-length", str(len(data)))
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(data)
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()

def run():
    server_address = '', 8000
    httpd = HTTPServer(server_address, RequestHandler)
    httpd.serve_forever()

if __name__ == "__main__":
    run()
