""" This is the entity, StaffProject"""
from staff import Staff
from project import Project


class StaffProject:

    def __init__(self):  # a method to create objects
        self.__project = Project()  # private attribute
        self.__staff = Staff()   # private attribute

    def get_project(self):  # get method
        return self.__project

    def set_project(self, a_project):  # set method
        self.__project = a_project

    def get_staff(self):  # get method
        return self.__staff

    def set_staff(self, person):  # set method
        self.__staff = person



