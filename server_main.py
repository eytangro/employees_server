# This is a REST server, written as a final exercise for Python course.
# This server handles employees DB and has an API according to requirements.
#
# Written by: David Sapir
# Date: 12 May 2019
from flask import Flask, jsonify
import employees_db
import employee
from flask import request
from logger import my_logger
import traceback

app = Flask(__name__)
# app.run(port=5002)

emps = employees_db.EmployeesDB('employesObj.json')


@app.route('/', methods=['GET'])
def hello_world():
    return {"data": 'The server is working :)',
    "message":"OK"}


@app.route('/all_names', methods=['GET'])
def get_names():
    all_emps = emps.get_all_employee_names()
    return {
        "message": "OK",
        "data":all_emps
    }


@app.route('/get_employee', methods=['GET'])
def get_employee():
    name = request.args.get("name")
    if name is None:
        return {"error": "Missing parameters 'name'"}
    try:
        emp = emps.get_employee(name)
    except Exception as ex:
        return {"error":  str(ex)}

    return {"message": "OK",
            "data": emp}


@app.route('/max_workers', methods=['POST','GET'])
def set_max_number_of_workers():
    if request.method=='POST':
        max_workers = request.json.get("max_workers")
        if max_workers is None:
            return {"error": "missing parameter, max_workers"}
        emps.set_max_workers_number(max_workers)
        return {
            "message": "OK",
            "data": request.json
        }
    elif request.method=='GET':
        return {
            "message":"OK",
            "data":emps.max_workers_number
        }




@app.route('/add_employee', methods=['POST'])
def add_employee():
    name = request.json.get("name")
    birthday = request.json.get("birthday")
    department = request.json.get("department")
    salary = request.json.get("salary")
    programs = request.json.get("programs")
    address = request.json.get("address")
    if name is None:
        return {"error": "Missing parameters 'name' and employee's info"}
    try:
        emp = employee.Employee(
            name, birthday, department, salary, programs, address)
        res = emps.add_emp(employee=emp)
    except Exception as ex:
        my_logger.error("Exception error: " + str(ex))
        return {"error: " + str(ex)}
    my_logger.info("result is " + str(res))
    if res is True:
        return {"message": "OK",
                "data": request.json}
    return {"error": "Error adding! " + res}


@app.route('/remove_employee', methods=['DELETE'])
def remove_employee():
    name = request.json.get("name")
    if name is None:
        return {"error": "Missing parameter 'name'"}
    try:
        res = emps.del_emp(name)
    except Exception as ex:
        my_logger.error("Exception error: " + str(ex))
        return {"error": "Exception error: " + str(ex)}
    my_logger.info("result is " + str(res))
    if res is True:
        return {"message": "OK",
                "data":{"deleted": request.json}}
    return {"error": "Error deleting! " + res}


@app.route('/update_employee_salary', methods=['POST'])
def update_employee_salary():
    name = request.json.get("name")
    salary = request.json.get("salary")
    if name is None or salary is None:
        return {"error": "Missing parameters 'name' or 'salary'"}
    try:
        res = emps.update_emp_salary(empName=name, newSalary=salary)
    except Exception as ex:
        my_logger.error("Exception error: " + str(ex))
        return {"error: " + str(ex)}
    my_logger.info("result is " + str(res))
    if res is True:
        return {"message": "OK",
                "data":{"updated": request.json}}
    return {"error": "error updating salary! " + res}


@app.route('/update_all_salary', methods=['POST'])
def update_all_salary():
    salaryIncrease = request.json.get("salary_increase")
    if salaryIncrease is None:
        return {"error": "Missing parameter 'salary_increase'"}
    try:
        res = emps.update_all_salaries(salaryIncrease)
    except Exception as ex:
        my_logger.error("Exception error: " + str(ex))
        return {"error": "Exception error: " + str(ex)}
    my_logger.info("result is " + str(res))
    if res is True:
        return {"message": "OK",
                "data":{"updated": request.json}}
    return {"error": "Error updating salary! " + res}


@app.route('/get_employee_by_birth_month', methods=['GET'])
def get_emp_by_birth_month():
    month = request.args.get("month")
    if month is None:
        return {"error": "Missing parameter 'month'"}
    try:
        res = emps.get_birth_month_emps(month)
    except Exception as ex:
        my_logger.error("Exception error: " + str(ex))
        return {"error": "Exception error: " + str(ex)}
    my_logger.info("result is " + str(res))
    return {"message": "OK",
            "data": res}


@app.route('/add_program_to_employee', methods=['POST'])
def add_program_to_employee():
    name = request.json.get("name")
    program = request.json.get("program")
    if name is None or program is None:
        return {"error": "Missing parameters 'name' 'program'"}
    try:
        res = emps.add_program_to_emp(empName=name, newProgram=program)
    except Exception as ex:
        my_logger.error("Exception error: " + str(ex))
        return {"error": "Exception error: " + str(ex)}
    my_logger.info("result is " + str(res))
    if res is True:
        return {"message": "OK",
                "data": request.json}
    return {"error": "Error adding program to employee! " + res}


@app.route('/delete_db', methods=['DELETE'])
def deleteDB():
    try:
        res = emps.deleteDB()
    except Exception as ex:
        my_logger.error("Exception error: " + str(ex))
        return {"error": "Exception error: " + str(ex)}
    my_logger.info("result is " + str(res))
    if res is True:
        return {"message": "OK"}
    return {"error": "Error deleting DB! " + res}


@app.route('/upload_db', methods=['POST'])
def uploadDB():
    newDB = request.json
    if not newDB:
        return {"error": "Missing payload for json DB"}
    try:
        res = emps.uploadDB(newDB)
    except ValueError as vex:
        my_logger.error("Error: " + str(vex))
        return {"error": + str(vex)}
    except Exception as ex:
        my_logger.error("Exception error: " + str(ex) + traceback.format_exc())
        return {"error": "Exception error: " + str(ex)}
    my_logger.info("result is " + str(res))
    if res is True:
        return {"message": "OK",
                "data": request.json}
    return {"error": "Error uploading DB! " + res}


def run_server():
    app.run(port=5002)


if __name__ == '__main__':

    run_server()
