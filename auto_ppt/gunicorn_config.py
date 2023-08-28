import os

bind = "0.0.0.0:5000"
workers = 4
env = {
    "FLASK_ENV": "test"
}
timeout = 600
