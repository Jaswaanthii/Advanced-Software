""" This is the entity, Project"""


class Project:

    def __init__(self):  # a method to create objects
        self.__name = ""  # private attribute
        self.__client_id = 0

    def get_name(self):  # get method
        return self.__name

    def set_name(self, team):  # set method
        self.__name = team

    def get_client_id(self):  # get method
        return self.__client_id

    def set_client_id(self, num):  # set method
        self.__client_id = num

