#!/bin/bash
# Entrypoint script: create tables, then start API
set -e

python db_manager.py
exec uvicorn api:app --host 0.0.0.0 --port 8000
