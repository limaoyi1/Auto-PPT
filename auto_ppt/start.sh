#!/bin/bash
nohup gunicorn -c gunicorn_config.py application:app  &
