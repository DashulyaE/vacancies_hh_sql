import psycopg2
from typing import List


def create_database(db_name: str, params: dict):
    """Создание базы данных для сохранения данных о компаниях и вакансиях"""

    conn = None
    try:
        conn = psycopg2.connect(dbname="postgres", **params)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
            cur.execute(f"CREATE DATABASE {db_name}")
    except psycopg2.Error as e:
        print("Ошибка подключения к базе данных")
        raise e
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
            cur.execute(
                """
                CREATE TABLE employers (
                    employers_id VARCHAR(25) PRIMARY KEY,
                    name VARCHAR(255),
                    url VARCHAR(255))
                """
            )

        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE vacancies (
                    vacancy_id VARCHAR(25) PRIMARY KEY,
                    name VARCHAR(255),
                    url VARCHAR(255),
                    employers_name VARCHAR(255),
                    employers_id VARCHAR(25),
                    CONSTRAINT fk_employers FOREIGN KEY (employers_id) REFERENCES employers(employers_id))
                """
            )
    except psycopg2.Error as e:
        print("Ошибка подключения к базе данных")
        raise e
    finally:
        if conn:
            conn.close()


def load_employers(db_name: str, params: dict, emp_list: list[dict]):
    """Загрузка компаний в базу данных в таблицу employers"""

    conn = None
    try:
        conn = psycopg2.connect(dbname=db_name, **params)
        conn.autocommit = True
        with conn.cursor() as cur:
            for employer in emp_list:
                cur.execute(
                    """
                INSERT INTO employers (employers_id, name, url)
                    VALUES (%s, %s, %s)
                """,
                    (employer["id"], employer["name"], employer["alternate_url"]),
                )
    except psycopg2.Error as e:
        print("Ошибка подключения к базе данных")
        raise e
    finally:
        if conn:
            conn.close()


def load_vacancies(db_name: str, params: dict, vac_list: List[dict]):
    """Загрузка вакансий для указанных компаний в базу данных в таблицу vacancies"""

    conn = None
    try:
        conn = psycopg2.connect(dbname=db_name, **params)
        conn.autocommit = True
        with conn.cursor() as cur:
            for vacancies in vac_list:
                if vacancies != []:
                    for vacancy in vacancies:
                        vacancy_id = vacancy.get("id", 0)
                        name = vacancy.get("name", 0)
                        url = vacancy.get("alternate_url", 0)
                        employers_name = vacancy.get("employer", 0).get("name")
                        employers_id = vacancy.get("employer", 0).get("id")

                        cur.execute(
                            """
                            INSERT INTO vacancies (vacancy_id, name, url, employers_name, employers_id)
                                VALUES (%s, %s, %s, %s, %s)
                            """,
                            (vacancy_id, name, url, employers_name, employers_id),
                        )

    except psycopg2.Error as e:
        print("Ошибка подключения к базе данных")
        raise e
    finally:
        if conn:
            conn.close()
