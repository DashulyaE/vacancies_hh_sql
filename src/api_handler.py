import requests
import os
from dotenv import load_dotenv


class HeadHunterAPI:
    """Класс для работы с вакансиями через API Head Hunter"""

    def __init__(self):
        self.url = "https://api.hh.ru/"

    def _connect_employer(self, employer_id: str):
        """Метод подключения к API для получения данных о компании"""

        response = requests.get(f"{self.url}/employers/{employer_id}")
        response_check = self._connect_check(response)
        return response_check

    def _connect_vacancy(self, employer_id: str):
        """Метод подключения к API для получения данных о вакансиях компании"""

        params = {"employer_id": employer_id}
        response = requests.get(f"{self.url}/vacancies", params=params)
        response_check = self._connect_check(response)
        return response_check

    def _connect_check(self, response):
        """Метод проверки запроса к API"""

        try:
            response
            if response.status_code == 200:
                return response
            else:
                raise Exception(f"Ошибка при обращении к API:, {response.status_code}")
        except Exception as e:
            print(f"Возникла ошибка при обращении к API , {e}")

    def get_employer(self, employer_list_id):
        """Метод получения списка компаний по id"""

        employer_list = []
        for employer in employer_list_id:
            response = self._connect_employer(employer)
            if response:
                employer = response.json()
                employer_list.append(employer)
                if employer_list == []:
                    print("Компании не найдены")
        return employer_list

    def get_vacancies(self, employer_list_id):
        """Метод получения списка вакансий по id компании"""

        vacancies_list = []
        for employer in employer_list_id:
            response = self._connect_vacancy(employer)
            if response:
                vacancies = response.json().get("items", [])
                vacancies_list.append(vacancies)
                if vacancies_list == [[]]:
                    print(f"Вакансии не найдены для компании {employer}")
        return vacancies_list


if __name__ == "__main__":
    load_dotenv()
    employers_id = os.getenv("employer_list_id")
    employers_lst_id = employers_id.split(",")
    employers_obj = HeadHunterAPI()
    employers_lst = employers_obj.get_employer(employers_lst_id)
    vacancies_list = employers_obj.get_vacancies(employers_lst_id)
    print(employers_lst)
    print(vacancies_list)
