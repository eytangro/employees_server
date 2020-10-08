# This class handles the employee DB. It performs all actions on DB.
#
# Written by: David Sapir
# Date: 12 May 2019

import datetime
import json
from logger import my_logger
import employee
from operator import itemgetter, attrgetter
import types


class EmployeesDB:
    emps = dict()

    def __init__(self, filename):
        self.filename = filename
        self.get_max_workers_number()
        try:
            with open(filename, 'r') as dbFile:
                self.emps = json.load(dbFile)
        except:
            self.emps = {"employees": {}}

    def get_max_workers_number(self):
        try:
            with open('max_workers_num.json', 'r')as f:
                self.max_workers_number = json.load(f)['max_workers']
        except:
            self.set_max_workers_number (15)

    def set_max_workers_number(self, max_workers):
        self.max_workers_number = max_workers
        with open('max_workers_num.json', 'w')as f:
            obj = {
                "max_workers": max_workers
            }
            json.dump(obj, f, indent=4)

    def save_db_2_file(self):
        with open(self.filename, 'w') as dbFile:
            json.dump(self.emps, dbFile, indent=4)
        my_logger.info("Data Saved")

    def get_all_employee_names(self):
        names = []
        for k in self.emps['employees'].keys():
            names.append(k)
        return names

    def get_employee(self, emp_name):
        return self.emps['employees'][emp_name]

    def add_emp(self, employee):
        my_logger.info("add_emp: " + employee.name)
        if employee.name in self.emps['employees'].keys():
            return "Employee exists"
        if self.emps['employees'].__len__() >= self.max_workers_number:
            return "Employee limit reached. Cannot add another one."
        if float(employee.salary) > 35000:
            return "Employee's salary is too high. Cannot add this employee."
        if int(datetime.datetime.now().year) - int(employee.birthday["year"]) > 65:
            return "Note employee's age. Consider retiring this employee."
        if len (employee.name)>10:
            return
        self.emps['employees'][employee.name] = employee.__dict__
        self.save_db_2_file()
        return True

    def del_emp(self, employeeName):
        my_logger.info("Delete Emp: " + employeeName)
        if employeeName not in self.emps['employees'].keys():
            return "Employee does not exist"
        del (self.emps['employees'][employeeName])
        self.save_db_2_file()
        return True

    def update_emp_salary(self, empName, newSalary):
        if float(newSalary) > 35000:
            return "Salary too high"
        for e in self.emps['employees']:
            currEmpName = self.emps['employees'].get(e).get('name')
            if empName == currEmpName:
                self.emps['employees'].get(e)['salary'] = newSalary
                self.save_db_2_file()
                return True
        return "Employee was not found"

    def update_all_salaries(self, increasePerCent):
        errMsg = ""
        for e in self.emps['employees']:
            currSalary = self.emps['employees'].get(e)['salary']
            newSalary = float(currSalary) * \
                (float(increasePerCent) / 100.0 + 1)
            if newSalary <= 35000:
                self.emps['employees'].get(e)['salary'] = newSalary
            else:
                errMsg += "Employee " + self.emps['employees'].get(e)['name'] + \
                          "'s salary would exceed. Therefore salary will not update. (Other employees' salary was updated.) "
        self.save_db_2_file()
        if len(errMsg) != 0:
            return errMsg
        return True

    def get_birth_month_emps(self, month):
        empList = []
        for e in self.emps['employees']:
            try:
                currBirthMonth = self.emps['employees'].get(
                    e)['birthday']['month']
                if int(currBirthMonth) == int(month):
                    empList.append(e)
            except Exception as ex:
                my_logger.error("Exception error: " + str(ex))
        return empList

    def add_program_to_emp(self, empName, newProgram):
        newProgram = newProgram.strip()
        for e in self.emps['employees']:
            currEmpName = self.emps['employees'].get(e).get('name')
            if empName == currEmpName:
                empPrograms = self.emps['employees'].get(e)['programs']
                if newProgram not in empPrograms:
                    if not empPrograms or empPrograms == "":
                        self.emps['employees'].get(e)['programs'] = newProgram
                    else:
                        self.emps['employees'].get(
                            e)['programs'].append(newProgram)
                    # Delete empty values
                    for i in range(len(empPrograms) - 1):
                        if empPrograms[i] == "":
                            del (empPrograms[i])
                    self.save_db_2_file()
                    return True
                else:
                    return "Program already exists"
        return "Employee was not found"

    def deleteDB(self):
        self.emps['employees'] = {}
        self.save_db_2_file()
        return True

    def uploadDB(self, newDB):
        self.emps = json.loads(json.dumps(newDB))  # re-parse the json input
        # self.emps = self.ParseInputDbData(data=newData)
        self.save_db_2_file()
        return True


    def get_emp_salary_sorted(self):
        empList = []
        for e in self.emps['employees']:
            empName = self.emps['employees'].get(e)['name']
            empSalary = self.emps['employees'].get(e)['salary']
            empList.append((empName, float(empSalary)))
        sortedList = sorted(empList, key=itemgetter(1, 0), reverse=True)
        sortedEmpsBySalary = {}
        sortedEmpsBySalary['salaries'] = sortedList
        return sortedEmpsBySalary

