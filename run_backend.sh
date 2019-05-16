#!/usr/bin/env bash

exec venv/bin/gunicorn run_backend:app -b 0.0.0.0:5000 --log-level debug 2>&1
