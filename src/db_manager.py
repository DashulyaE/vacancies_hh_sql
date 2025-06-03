import psycopg2


class DBManager:
    """Класс для взаимодейтсвия пользователя с базой данных"""
    def __init__(self, db_name: str, params: dict):
        """Инициализация класса, установка соединения с БД"""
        try:
            self.connection = psycopg2.connect(dbname=db_name, **params)
        except psycopg2.Error as e:
            print(f"Ошибка при подключении к БД: {e}")


    def close_connection(self) -> None:
        """Закрытие соединения с БД."""
        if self.connection:
            self.connection.close()


    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""

        with self.connection.cursor() as cursor:
            cursor.execute(
                """SELECT e.name, COUNT(v.vacancy_id) AS vacancy_count 
                FROM employers e
                LEFT JOIN vacancies v USING(employers_id)
                GROUP BY e.name;
                """
            )
            data = cursor.fetchall()
            if data:
                return data



    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, вакансии и зарплаты и ссылки на вакансию"""

        with self.connection.cursor() as cursor:
            cursor.execute(
                """SELECT e.name, v.name, v.salary, v.url
                FROM employers e
                INNER JOIN vacancies v USING(employers_id)
                """
            )
            data = cursor.fetchall()
            if data:
                return data


    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        with self.connection.cursor() as cur:
            cur.execute(
                """
              SELECT AVG(salary) FROM vacancies;"""
            )
            data = cur.fetchone()[0]
        return round(data, 2) if data is not None else None


    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        avg_salary = self.get_avg_salary()
        if avg_salary is None:
            return []

        with self.connection.cursor() as cur:
            cur.execute("""SELECT * FROM vacancies WHERE salary > (SELECT AVG(salary) FROM vacancies)""")
            data = cur.fetchall()
        return data

    def get_vacancies_with_keyword(self, keyword: str):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        with self.connection.cursor() as cur:
            cur.execute(
                """SELECT * FROM vacancies WHERE name LIKE %s;""",
                (f"%{keyword}%",),
            )
            data = cur.fetchall()
            return data
