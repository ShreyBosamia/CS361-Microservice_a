import psycopg2
from dotenv import dotenv_values
from pathlib import Path

env = dotenv_values(dotenv_path=Path('./.env'))


# Connect to the database (local PostgreSQL)
def get_local_db_connection():
    connection = psycopg2.connect(
        dbname=env['LOCAL_DB_NAME'],
        user=env['LOCAL_DB_USER'],
        password=env['LOCAL_DB_PASSWORD'],
        host=env['LOCAL_DB_HOST'],
        port=env['LOCAL_DB_PORT']
    )
    return connection
