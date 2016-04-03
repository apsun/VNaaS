#!/usr/bin/env python3
import sys
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from . import vnaas


def main():
    if len(sys.argv) not in (2, 3):
        print("usage: python3 wsgi.py database.db [port]")
        return

    app = vnaas.app
    app.config["DATABASE_PATH"] = sys.argv[1]
    http_server = HTTPServer(WSGIContainer(app))
    port = 5000
    if len(sys.argv) == 3:
        port = int(sys.argv[2])
    http_server.listen(port)
    IOLoop.instance().start()


if __name__ == "__main__":
    main()
