"""Settings - edit these (or set the same names as environment variables)."""
import os
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "1234")          # <- your MySQL password
DB_NAME = os.getenv("DB_NAME", "rice_quality")
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key")
