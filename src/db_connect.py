import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.errorcodes import INVALID_CATALOG_NAME


def create_database(db_name: str, params: dict):
    """Создание базы данных для сохранения данных о компаниях и вакансиях"""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cur.execute(f"CREATE DATABASE {db_name}")
    cur.close()
    conn.close()
