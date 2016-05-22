from __future__ import absolute_import, print_function
import socket
import os
import signal
import sys
import cgi
import argparse

if sys.version_info >= (3, 0):
    from http.server import SimpleHTTPRequestHandler
    import socketserver
    from urllib.parse import urlparse
else:
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    import SocketServer as socketserver
    from urlparse import urlparse

def main():
    parser = argparse.ArgumentParser(description="demo web server")
    parser.add_argument("-p", "--port", type=int, default=8000, help="port number for the server (default 8000)")
    args = parser.parse_args()

    here = os.path.dirname(__file__)
    docroot = os.path.relpath(os.path.join(here, "docroot"))
    os.chdir(docroot)

    try:
        httpd = DemoServer(("", args.port), DemoHandler)
        print("serving %s on port %s" % (docroot, 8000))
        print ("^C, or visit http://localhost:%s/admin/shutdown to stop" % args.port)
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

class DemoHandler(SimpleHTTPRequestHandler):

    def redirect(self, uri):
        self.send_response(301)
        self.send_header('Location', uri)
        self.end_headers()

    def do_POST(self):
        if self.path.startswith("/authenticate"):
            form = self.get_form_data()
            if "password" in form and form["password"].value == "password":
                self.redirect("/homepage.html")
            else:
                self.redirect("/login.html")

    def do_GET(self):
        url = urlparse(self.path)
        print("url: '%s' url.path: '%s'" % (url, url.path))
        if url.path == "" or url.path == "/" :
            self.redirect("/login.html")

        if url.path == "/authenticate":
            self.redirect("/homepage.html")
            return

        if url.path == '/admin/shutdown':
            print("server shutdown has been requested")
            os.kill(os.getpid(), signal.SIGHUP)

        return SimpleHTTPRequestHandler.do_GET(self)

    def get_query_parameters(self):
        idx = self.path.find("?")
        args = {}
        if idx >= 0:
            args = urlparse.parse_qs(self.path[idx+1:])
        return args

    def get_form_data(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                 })
        return form

class DemoServer(socketserver.TCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

if __name__ == "__main__":
    main()
