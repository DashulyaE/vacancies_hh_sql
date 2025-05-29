from config import config
import  re

from src.db_connect import create_database


def main():
    """Основная функция, обединяющая общую логику программы"""

    params = config()
    reg = re.compile(r'[a-zA-Z]')

    while True:
        db_name = input("Введите имя создаваемой базы данных: ")
        if reg.match(db_name):
            create_database(db_name, params)
            break
        else:
            print("Имя базы должно быть на английском языке")

if __name__ == "__main__":
    main()
