import os

from dotenv import load_dotenv

from config import config
import re

from src.api_handler import HeadHunterAPI
from src.db_connect import create_database, create_table, load_employers, load_vacancies
from src.db_manager import DBManager


def main():
    """Основная функция, обединяющая общую логику программы"""

    params = config()
    reg = re.compile(r"[a-zA-Z]")

    while True:
        db_name = input("Введите имя создаваемой базы данных: ")
        if reg.match(db_name):
            create_database(db_name, params)
            create_table(db_name, params)
            load_dotenv()
            employers_id = os.getenv("employer_list_id")
            employers_lst_id = employers_id.split(",")
            employers_obj = HeadHunterAPI()
            employers_lst = employers_obj.get_employer(employers_lst_id)
            vacancies_list = employers_obj.get_vacancies(employers_lst_id)
            load_employers(db_name, params, employers_lst)
            load_vacancies(db_name, params, vacancies_list)

            db_obj = DBManager(db_name, params)

            print("Выберите необходимые действия с БД:")

            answer_1 = (input("Вывести на экран работодателей с кол-вом вакансий (да/нет): ")).lower()
            if answer_1 in ["да", "yes"]:
                comp_vac = db_obj.get_companies_and_vacancies_count()
                for rezult in comp_vac:
                    print(f"""Работодатель - {rezult[0]}: {rezult[1]} вакансий""")

            answer_2 = (input("Вывести на экран все вакансии (да/нет): ")).lower()
            if answer_2 in ["да", "yes"]:
                vacancies_all = db_obj.get_all_vacancies()
                for rezult in vacancies_all:
                    print(rezult)

            answer_3 = (input("Вывести на экран среднюю зарплату (да/нет): ")).lower()
            if answer_3 in ["да", "yes"]:
                average_salary = db_obj.get_avg_salary()
                print(f"Средняя зарплата по вакансиям: {average_salary}")

            answer_4 = (input("Вывести на экран все вакансии с з/п выше средней (да/нет): ")).lower()
            if answer_4 in ["да", "yes"]:
                higher_salary = db_obj.get_vacancies_with_higher_salary()
                for rezult in higher_salary:
                    print(rezult)

            answer_5 = (input("Сделать фильтрацию вакансий по ключевому слову (да/нет): ")).lower()
            if answer_5 in ["да", "yes"]:
                answer_6 = (input("Введите ключевой слово: ")).lower()
                vacancies_word = db_obj.get_vacancies_with_keyword(answer_6)
                for rezult in vacancies_word:
                    print(rezult)
            db_obj.close_connection()
            break
        else:
            print("Имя базы должно быть на английском языке")


if __name__ == "__main__":
    main()
