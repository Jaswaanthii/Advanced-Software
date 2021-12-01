
from contract import Contract
from profile import Profile
from datetime import date


class Staff:

    def __init__(self):  # a method to create objects
        self.__username = ""
        self.__email = ""
        self.__start_year = ""
        self.__role = ""
        self.__profile = Profile()
        self.__contract = Contract()

    def get_user_name(self):  # get method
        return self.__username

    def set_user_name(self, name):  # set method
        self.__username = name

    def get_email(self):  # get method
        return self.__email

    def set_email(self, mail):  # set method
        self.__email = mail

    def get_start_year(self):  # get method
        return self.__start_year

    def set_start_year(self, year):  # set method
        self.__start_year = year

    def get_work_years(self):
        start_year = int(self.__start_year)
        today_year = date.today().year
        year = today_year - start_year
        return year

    def get_role(self):  # get method
        return self.__role

    def set_role(self, a_role):  # set method
        self.__role = a_role

    def get_profile(self):  # get method
        return self.__profile

    def set_profile(self, the_type):  # composition
        self.__profile.set_username(self.__username)
        self.__profile.set_type(the_type)

    def get_contract(self):  # get method
        return self.__contract

    def set_contract(self, pay):  # composition
        self.__contract.set_username(self.__username)
        self.__contract.set_pay(pay)


if __name__ == "__main__":
    staff = Staff()
    staff.set_start_year("2011")  # 01/01/2011
    result = staff.get_work_years()
    print("result: " + str(result))
