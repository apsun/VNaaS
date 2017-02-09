#!/usr/bin/env python
import sys
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import vnaas

PORT = 8080

def main():
    if len(sys.argv) == 1:
        port = PORT
    elif len(sys.argv) == 2:
        port = int(sys.argv[1])
    else:
        print("usage: wsgi.py [port]")
        return
    http_server = HTTPServer(WSGIContainer(vnaas.app))
    http_server.listen(port)
    IOLoop.instance().start()


if __name__ == "__main__":
    main()
