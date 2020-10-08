# This class handles the employee. It parses the input to an object
#
# Written by: David Sapir
# Date: 12 May 2019

from logger import my_logger


class Employee:
    def __init__(self, name, birthday, department, salary, programs, address):
        if name:
            self.name = name
        else:
            self.name = 'NA'
        self.birthday = Birthday(birthday).__dict__
        if department:
            self.department = department
        else:
            self.department = 'NA'
        if salary:
            self.salary = salary
        else:
            self.salary = 0
        self.programs = self.parse_programs(programs)
        if address:
            self.address = address
        else:
            self.address = 'NoWhere'
        my_logger.info("Parsed employee: " + str(self.__dict__))

    def parse_birthday(self, birthdate):
        bdate = Birthday(birthdate)
        return bdate.__dict__

    def is_birthday(self, month):
        if self.birthday['month'] == month:
            return True
        return False

    def parse_programs(self, programs):
        my_logger.info("Got programs: " + str(programs))
        if not programs:
            progArray = []
        else:
            dummyStr = ""
            dummyDict = {}
            dummyList = []
            if type(programs) == type(dummyStr):
                programs = programs.replace('[', '').replace(']', '')
                progArray = programs.split(",")
                for i in range(len(progArray)):
                    progArray[i] = progArray[i].strip()
            elif type(programs) == type(dummyDict):
                pass
            elif type(programs) == type(dummyList):
                progArray = programs
            else:
                progArray = []
        my_logger.info("Parsed programs: " + str(progArray))
        return progArray


class Birthday:
    def __init__(self, birthdate):
        my_logger.info("Got birthday: " + str(birthdate))
        if birthdate:
            dummyStr = ""
            dummyDict = {}
            if type(birthdate) == type(dummyStr):
                bdate = birthdate.split('-')
                if bdate.__len__() >= 3:
                    self.day = bdate[0]
                    self.month = bdate[1]
                    self.year = bdate[2]
                    return
            if type(birthdate) == type(dummyDict):
                self.day = birthdate.get('day')
                self.month = birthdate.get('month')
                self.year = birthdate.get('year')
                return
        self.day = 1
        self.month = 1
        self.year = 1970
