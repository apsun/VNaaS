# VNaaS web server

The actual web server for VNaaS. Can either be deployed
locally or on Google App Engine.

If you are deploying on GAE, you must use the Python data
option. Otherwise, you can choose either SQLite or Python.
The SQLite option is a bit slower, but uses considerably
less RAM.

## Local deployment

1. Download the dependencies
 - `pip install flask tornado`

2. Run the server (port defaults to 8080 if not specified)
 - `python wsgi.py [port]`

## Google App Engine deployment

1. Download the dependencies
 - `pip install --target=lib flask`

2. Deploy to GAE
 - `gcloud app deploy app.yaml`
