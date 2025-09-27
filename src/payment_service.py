"""
Mock Payment Service using a Service-Oriented Architecture
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
import os
import xml.etree.ElementTree as ET
from urllib.parse import parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
from views.template_view import show_404_page, xml_to_dict
from views.payment_view import add_payment, pay, show_payment_form


class PaymentServiceSOA(BaseHTTPRequestHandler):
    def do_GET(self):
        """ Handle GET requests received by the http.server """
        if self.path == "/" or self.path == "/home":
            self._send_html("<h1>PaymentServiceSOA</h1>")
            return
        elif self.path.startswith("/payments/pay"):
            id = self.path.split("/")[-1]
            response = show_payment_form(id)
            self._send_html(response)
        elif "/assets" in self.path: # load assets such as images, CSS, etc.
            self.load_asset()      
        else:
            self._send_html(show_404_page(), status=404)

    def do_POST(self):
        """ Handle POST requests received by the http.server """
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode("utf-8")

        # Parse XML instead of query string
        try:
            # TODO: go to middleware, then "resolve_route"
            root = ET.fromstring(body)
            params = xml_to_dict(root)
        except ET.ParseError as e:
            # Handle XML parsing error
            params = {}
        if self.path == "/payments/add":
            response = add_payment(params)
            self._send_html(response)
        elif self.path.startswith("/payments/pay"):
            id = self.path.split("/")[-1]
            response = pay(id)
            self._send_html(response)
        else:
            self._send_html(show_404_page(), status=404)

    def load_asset(self):
        """ Load assets from disk based on requested path, then send file contents as a response to the client """
        path_parts = self.path.split(".")
        extension = path_parts[1] if len(path_parts) >= 2 else None
        base_directory = os.path.dirname(__file__)
        with open(base_directory + self.path, "r") as file:
            css = "".join(file.readlines())
            self.send_response(200)
            self.send_header("Content-type", self.get_mimetype(extension))
            self.end_headers()
            self.wfile.write(css.encode("utf-8"))

    def get_mimetype(self, extension):
        """ Get mimetype (https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/MIME_types/Common_types) """
        if (extension == "html"):
            return "text/html"
        elif (extension == "css"):
            return "text/css"
        elif (extension == "js"):
            return "text/javascript"
        elif (extension == "svg"):
            return "image/svg+xml"
        else:
            return "application/octet-stream"

    def _send_html(self, html, status=200):
        """ Send given HTML string as a response to the client """
        self.send_response(status)
        self.send_header("Content-type", self.get_mimetype("html"))
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 5009), PaymentServiceSOA)
    print("Server running on http://0.0.0.0:5009")
    server.serve_forever()
