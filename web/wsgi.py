#!/usr/bin/env python
import sys
import gevent.wsgi
import vnaas

PORT = 8080

if __name__ == "__main__":
    if len(sys.argv) == 1:
        port = PORT
    elif len(sys.argv) == 2:
        port = int(sys.argv[1])
    else:
        print("usage: wsgi.py [port]")
    http_server = gevent.wsgi.WSGIServer(("0.0.0.0", port), vnaas.app)
    http_server.serve_forever()
