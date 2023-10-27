# myapp_config.py
wsgi_app = "flove_blog.wsgi:application"
bind = "127.0.0.1:8000"
workers = 4
timeout = 60
loglevel = "debug"
reload = True
daemon = True
