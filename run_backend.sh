#!/usr/bin/env bash

exec venv/bin/gunicorn run_backend:app 2>&1
