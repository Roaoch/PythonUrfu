from input_connect import InputConnect
from report import Report
from errors import OutOfDataError


try:
    input_connect = InputConnect(
        input("Введите название файла: "),
        input("Введите название профессии: ")
    )
    report = Report()

    report.generate_excel(
        input_connect.all_salary_level,
        input_connect.all_vacancies_count,
        input_connect.salary_level,
        input_connect.vacancies_count,
        input_connect.by_city_level,
        input_connect.vacancies_part
    )
    report.generate_image(
        input_connect.filter_parameter,
        input_connect.all_salary_level,
        input_connect.all_vacancies_count,
        input_connect.salary_level,
        input_connect.vacancies_count,
        input_connect.by_city_level,
        input_connect.vacancies_part
    )
    report.generate_pdf(input_connect.filter_parameter)
    input_connect.print_self()
except StopIteration:
    print("Пустой файл")
except IOError:
    print("Формат ввода некорректен")
except KeyError:
    print("Параметр поиска некорректен")
except AssertionError:
    print("Ничего не найдено")
except OutOfDataError:
    print("Нет данных")
