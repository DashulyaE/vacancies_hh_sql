from typing import Any

import requests
from abc import ABC, abstractmethod


class BaseApi(ABC):
    """Абстрактный класс для работы с API"""

    @abstractmethod
    def _connect_employer(self, employer_id: str):
        """Абстрактный метод подключения к API для получения данных о компании"""
        pass

    @abstractmethod
    def _connect_vacancy(self, employer_id: str):
        """Абстрактный метод подключения к API для получения данных о вакансиях компании"""
        pass

    def _connect_check(self):
        """Абстрактный метод проверки запроса к API"""
        pass


class HeadHunterAPI(BaseApi):
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

    def get_employer(self, employer_list_id: list):
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

    def get_vacancies(self, employer_list_id: list):
        """Метод получения списка вакансий по id компании"""

        vacancies_list = []
        for employer in employer_list_id:
            response = self._connect_vacancy(employer)
            if response:
                vacancies = response.json().get("items", [])
                vacancies_list.append(vacancies)
        return vacancies_list
