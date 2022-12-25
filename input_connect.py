from data_set import DataSet
from utils import Utils
from typing import Dict


class InputConnect:
    def __init__(
            self,
            filename,
            filter_parameter
    ):
        self.__vacancies = DataSet(file_name=filename.strip())
        self.filter_parameter = filter_parameter.strip()
        self.all_salary_level = {}
        self.all_vacancies_count = {}
        self.salary_level = {}
        self.vacancies_count = {}
        self.by_city_level = {}
        self.vacancies_part = {}
        self.__get_statistics()

    def __get_statistics(self) -> None:
        temp_by_city_count = {}
        temp_by_city_level = {}
        temp_all_by_city_count = {}
        for vacancy in self.__vacancies.vacancies_reader:
            vacancy_year = vacancy.published_at.year
            vacancy_salary = vacancy.salary.get_salary()
            Utils.add_to_or_update(
                self.all_salary_level,
                vacancy_year,
                vacancy_salary
            )
            Utils.add_to_or_update(
                self.all_vacancies_count,
                vacancy_year,
                1
            )
            Utils.add_to_or_update(
                temp_by_city_level,
                vacancy.area_name,
                vacancy_salary
            )
            Utils.add_to_or_update(
                temp_all_by_city_count,
                vacancy.area_name,
                1
            )
            if self.filter_parameter in vacancy.name:
                Utils.add_to_or_update(
                    self.salary_level,
                    vacancy_year,
                    vacancy_salary
                )
                Utils.add_to_or_update(
                    self.vacancies_count,
                    vacancy_year,
                    1
                )
                Utils.add_to_or_update(
                    temp_by_city_count,
                    vacancy.area_name,
                    1
                )
        self.all_salary_level = {
            key: int(value / self.all_vacancies_count[key]) for key, value in self.all_salary_level.items()
        }
        self.salary_level = {
            key: int(value / self.vacancies_count[key]) for key, value in self.salary_level.items()
        }

        if len(self.salary_level) == 0:
            self.salary_level = {key: 0 for key in self.all_vacancies_count.keys()}
            self.vacancies_count = {key: 0 for key in self.all_vacancies_count.keys()}

        self.vacancies_part = self.__get_vacancy_part(temp_all_by_city_count)
        self.by_city_level = dict(sorted(
            [(key, int(temp_by_city_level[key] / temp_all_by_city_count[key])) for key in self.vacancies_part.keys()],
            key=lambda e: (e[1], -len(e[0])),
            reverse=True
        ))

    def print_self(self) -> None:
        print(f"Динамика уровня зарплат по годам: {self.all_salary_level}")
        print(f"Динамика количества вакансий по годам: {self.all_vacancies_count}")
        print(f"Динамика уровня зарплат по годам для выбранной профессии: {self.salary_level}")
        print(f"Динамика количества вакансий по годам для выбранной профессии: {self.vacancies_count}")
        print(f"Уровень зарплат по городам (в порядке убывания): {Utils.slice_dict(self.by_city_level, 10)}")
        print(f"Доля вакансий по городам (в порядке убывания): {Utils.slice_dict(self.vacancies_part, 10)}")

    @staticmethod
    def __get_vacancy_part(by_city_count: Dict[str, int]):
        result = []
        all_vacancy_count = sum(by_city_count.values())
        for key, value in by_city_count.items():
            part = value / all_vacancy_count
            if part >= 0.01:
                result.append((key, float("{:.4f}".format(part))))
        return dict(sorted(
            result,
            key=lambda e: e[1],
            reverse=True
        ))
