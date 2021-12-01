""" This is the entity, Advisor"""
from staff import Staff


class Advisor(Staff):

    def __init__(self):
        super().__init__()
        self.__remote = "London"  # default company location

    def get_remote(self):
        return self.__remote

    def set_remote(self, content):
        self.__remote = content
