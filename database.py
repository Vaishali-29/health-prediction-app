
import os
import sqlite3
from pathlib import Path

import psycopg
from psycopg.rows import dict_row


BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / "instance"
DATABASE_PATH = INSTANCE_DIR / "health.db"


class PostgresConnection:
    """Compatibility wrapper for existing SQLite-style queries."""

    def __init__(self, connection):
        self.connection = connection

    def execute(self, query, params=None):
        query = query.replace("?", "%s")
        return self.connection.execute(query, params or ())

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()


def get_connection():
    """Connect to Neon PostgreSQL or local SQLite."""

    database_url = os.getenv("DATABASE_URL")

    if database_url:
        connection = psycopg.connect(
            database_url,
            row_factory=dict_row
        )
        return PostgresConnection(connection)

    INSTANCE_DIR.mkdir(exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def init_db():
    """Create the patients table if it does not exist."""

    connection = get_connection()

    try:
        if os.getenv("DATABASE_URL"):
            connection.execute("""
                CREATE TABLE IF NOT EXISTS patients (
                    id BIGSERIAL PRIMARY KEY,
                    full_name TEXT NOT NULL,
                    dob TEXT NOT NULL,
                    email TEXT NOT NULL,
                    glucose DOUBLE PRECISION NOT NULL,
                    haemoglobin DOUBLE PRECISION NOT NULL,
                    cholesterol DOUBLE PRECISION NOT NULL,
                    remarks TEXT
                )
            """)
        else:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS patients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    dob TEXT NOT NULL,
                    email TEXT NOT NULL,
                    glucose REAL NOT NULL,
                    haemoglobin REAL NOT NULL,
                    cholesterol REAL NOT NULL,
                    remarks TEXT
                )
            """)

        connection.commit()

    finally:
        connection.close()

