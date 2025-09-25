import os, time
from datetime import datetime
from PynexDB import Pynex
pydb, pytb = Pynex.PyDb, Pynex.PyTb

_DB_FILE = 'Company_Employees.db'
_TB_NAME = 'Employees'

def return_datetime():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


db: pydb = Pynex.PyDb()
if _TB_NAME not in db.tables: db.table(_TB_NAME)

tb1: pytb = db[_TB_NAME]
if not os.path.exists(_DB_FILE):
    tb1.insert(employee_id=1, created=return_datetime(),
               first_name='John', last_name='Smith',
               email='john@company.com', position='owner')
    time.sleep(1)
    tb1.insert(employee_id=2, created=return_datetime(),
               first_name='Robert', last_name='Jones',
               email='bob.jones@company.com', position='vp')
    db.save(_DB_FILE, True)
db.load(_DB_FILE, True)
employees: pytb = db[_TB_NAME]
all_employees: list = employees.get_all()

print(len(employees))
