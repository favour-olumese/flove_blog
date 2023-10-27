"""Gunicorn development config file"""
import multiprocessing


# Django WSGI application path
wsgi_app = "flove_blog.wsgi:application"

# Error log outpuy
loglevel = "debug"

# The socket to bind
bind = "0.0.0.0:8000"

# Number of worker processes fro handling requests
workers = multiprocessing.cpu_count() * 2 + 1

# Restart workers when code changes (development only)
reload = True

# Access log
accesslog = "/var/log/gunicorn/dev.log"

# Error log
errorlog = "/var/log/gunicorn/dev.log"

# Redirect stdout/stderr to log file
capture_output = True

# PID file so you can easily fetch process ID
pidfile = "/var/run/gunicorn/dev.pid"

# Daemonize the Gunicorn process (Detach & enter background)
daemon = True