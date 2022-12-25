from salary import Salary
from typing import List
from datetime import datetime


class Vacancy:
    def __init__(self, property_list: List[any], headline: List[str]):
        if len(headline) == 12:
            self.name = property_list[0]
            self.description = property_list[1]
            self.key_skills = property_list[2] if type(property_list[2]) == list else [property_list[2]]
            self.experience_id = property_list[3]
            self.premium = property_list[4]
            self.employer_name = property_list[5]
            self.salary = Salary(property_list[6:10])
            self.area_name = property_list[10]
            self.published_at = datetime.strptime(property_list[11], "%Y-%m-%dT%H:%M:%S%z")
        elif len(headline) == 6:
            self.name = property_list[0]
            self.salary = Salary(property_list[1:4])
            self.area_name = property_list[4]
            self.published_at = datetime.strptime(property_list[5], "%Y-%m-%dT%H:%M:%S%z")