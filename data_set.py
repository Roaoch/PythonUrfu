import csv
import codecs
import re
from vacancy import Vacancy
from errors import OutOfDataError
from typing import List, Generator


class DataSet:
    __CLEANER = re.compile('<.*?>')
    __SPACE_CLEANER = re.compile('(\s\s+)|(\xa0)')

    def __init__(self, file_name: str):
        self.file_name = file_name
        self.headline = []
        self.vacancies_reader = self.__clean_properties(
            vacancies=self.__reader(file_name=file_name)
        )

    def __reader(self, file_name: str) -> csv.reader:
        reader = csv.reader(codecs.open(file_name, "r", "utf_8_sig"), delimiter=',')
        self.headline = reader.__next__()
        return reader

    def __validate(self, element: List[str]) -> bool:
        if len(element) != len(self.headline):
            return False
        for i in range(len(element)):
            if element[i] == '':
                return False
        return True

    def __clean_properties(self, vacancies: csv.reader) -> Generator[Vacancy, None, None]:
        i = 0
        key_skills_index = self.headline.index("key_skills") if "key_skills_index" in self.headline else -1
        for vacancy in vacancies:
            i += 1
            clean_vacancy = []
            if self.__validate(element=vacancy):
                for merit_index in range(len(vacancy)):
                    if merit_index == key_skills_index:
                        temp_property = vacancy[merit_index].split('\n')
                        for i in range(len(temp_property)):
                            temp_property[i] = re.sub(self.__CLEANER, '', temp_property[i])
                            temp_property[i] = re.sub(self.__SPACE_CLEANER, ' ', temp_property[i]).strip()
                    else:
                        temp_property = re.sub(self.__CLEANER, '', vacancy[merit_index])
                        temp_property = re.sub(self.__SPACE_CLEANER, ' ', temp_property).strip()
                    clean_vacancy.append(temp_property)
                yield Vacancy(clean_vacancy, self.headline)
        if i == 0:
            raise OutOfDataError