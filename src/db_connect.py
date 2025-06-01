import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.errorcodes import INVALID_CATALOG_NAME


def create_database(db_name: str, params: dict):
    """Создание базы данных для сохранения данных о компаниях и вакансиях"""

    conn = None
    try:
        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
            cur.execute(f"CREATE DATABASE {db_name}")
    except psycopg2.Error as e:
        print("Ошибка подключения к базе данных")
        raise
    finally:
        if conn:
            conn.close()

def create_table(db_name: str, params: dict):
    """Создание таблицы employers и vacancies со списком компаний и вакансий в базе данных"""

    conn = None
    try:
        conn = psycopg2.connect(dbname=db_name, **params)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE employers (
                    employers_id VARCHAR(25) PRIMARY KEY,
                    name VARCHAR(255),
                    url VARCHAR(255),
                    open_vacancies INTEGER                
                )            
        """)
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE vacancies (
                    vacancy_id VARCHAR(25) PRIMARY KEY,
                    name VARCHAR(255),
                    url VARCHAR(255),
                    employers_id VARCHAR(25),
                    CONSTRAINT fk_employers FOREIGN KEY (employers_id) REFERENCES employers(employers_id))            
            """)
    except psycopg2.Error as e:
        print("Ошибка подключения к базе данных")
        raise
    finally:
        if conn:
            conn.close()


def load_employers(db_name: str, params: dict, emp_list: list):
    """Загрузка компаний в базу данных в таблицу employers"""
    pass


def load_vacancies():
    """Загрузка вакансий для указанных компаний в базу данных в таблицу vacancies"""
    pass