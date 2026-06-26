#!/bin/bash
pip install uvicorn fastapi sqlalchemy psycopg2-binary python-dotenv python-jose passlib bcrypt python-multipart
uvicorn main:app --host 0.0.0.0 --port 8000
