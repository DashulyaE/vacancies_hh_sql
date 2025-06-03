import os

from dotenv import load_dotenv

from config import config
import  re

from src.api_handler import HeadHunterAPI
from src.db_connect import create_database, create_table, load_employers, load_vacancies
from src.db_manager import DBManager


def main():
    """Основная функция, обединяющая общую логику программы"""

    params = config()
    reg = re.compile(r'[a-zA-Z]')

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

            comp_vac = db_obj.get_companies_and_vacancies_count()
            vacancies_all = db_obj.get_all_vacancies()
            average_salary = db_obj.get_avg_salary()
            higher_salary = db_obj.get_vacancies_with_higher_salary()
            vacancies_word = db_obj.get_vacancies_with_keyword("Аналитик")
            for rezult in comp_vac:
                print(f"""Работодатель - {rezult[0]}: {rezult[1]} вакансий""")

            for rezult in vacancies_all:
                print(rezult)

            print(f"Средняя зарплата по вакансиям: {average_salary}")

            for rezult in higher_salary:
                print(rezult)

            for rezult in vacancies_word:
                print(rezult)
            break
        else:
            print("Имя базы должно быть на английском языке")

if __name__ == "__main__":
    main()
