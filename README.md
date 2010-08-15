# Hashfeedr

Django/Twisted app that streams tweets in real-time. Created in the light of
the Django Dash 2010 by @thedjinn, @michielheijkoop and @pnoordhuis.

## Setting up

Short explanation to get you up and running.

### Requirements

To setup and run the hashfeedr app, we recommend using a virtual environment.
Once setup, install the required packages by running:

		pip install -r requirements

Make sure to rehash (or restart) your terminal session to make sure the pip
installed executables (`twistd`, `gunicorn_django`) point to the virtualenv
environment.

The only external requirement is [Redis](http://redis.io). Hashfeedr is
configured to connect to Redis on localhost, port 6379 (the default).

### Instructions

There are three different components that need to be run, being:

* The Twitter streaming API consumer
* Twitter <-> WebSocket gateway
* Django app

The Twitter consumer can be started by changing your working directory to
`./twisted` and executing:

    TWUSER=xxx TWPASS=xxx twistd --pidfile tw.pid -ny producer/producer.py

Replace the `TWUSER` and `TWPASS` by valid Twitter credentials. This is
required because the streaming API requires authentication.

The Twitter <-> WebSocket gateway can by started from the same working
directory, by executing:

    twistd --pidfile ws.pid -ny consumer/wsserver.py
    
**Note:** Connecting to a WebSocket using the flash fallback (Firefox, IE)
requires a `crossdomain.xml` file to be served on port 843. This file located
in the `./media` folder. Browsers that do support WebSockets (WebKit) work
out of the box.

To start the Django app, first make sure so change the `WEBSOCKET_URL` variable
in `./djangostuff/settings.py` to match your testing environment (e.g. change
the host to be the server running twisted). Next, the Django app can be booted by changing
your working directory to `./djangostuff` and executing:

    gunicorn_django

If all was good, you're set up and ready to go. Point your browser to
[http://localhost:8000](http://localhost:8000) and enjoy!
