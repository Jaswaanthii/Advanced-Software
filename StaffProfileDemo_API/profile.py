""" This is the entity, Profile"""


class Profile:

    def __init__(self):  # a method to create objects
        self.__username = ""
        self.__type = ""

    def get_username(self):  # get method
        return self.__username

    def set_username(self, name):  # set method
        self.__username = name

    def get_type(self):  # get method
        return self.__type

    def set_type(self, content):  # set method
        self.__type = content

