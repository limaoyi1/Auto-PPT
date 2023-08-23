#!/bin/bash
nohup gunicorn -c gunicorn_config.py application:app > /dev/null 2>&1 &
