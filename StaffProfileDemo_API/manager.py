""" This is the entity, Manager"""
from staff import Staff


class Manager(Staff):

    def __init__(self):
        super().__init__()
        self.__bonus = 0.0

    def get_bonus(self):
        return self.__bonus

    def set_bonus(self, amount):
        self.__bonus = amount




