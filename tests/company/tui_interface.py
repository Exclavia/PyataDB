import os, time
from datetime import datetime
from PynexDB import Pynex
pydb, pytb = Pynex.PyDb, Pynex.PyTb

_DB_FILE = 'Company_Employees.db'
_TB_NAME = 'Employees'

def formatted_dt():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def new_employee(database: pydb, table: pytb, f_name: str, l_name: str, e_mail: str, pos: str):
    next_id = len(table) + 1
    table.insert(employee_id=next_id,
                 created=formatted_dt(),
                 first_name=f_name,
                 last_name=l_name,
                 email=e_mail,
                 position=pos)
    database.save(_DB_FILE)
    print(f'\nEmployee #{next_id} added')
    return next_id

def main(): 
    db: pydb = Pynex.PyDb()
    db.load(_DB_FILE)
    tb1: pytb = db[_TB_NAME]
    print('')
    print('1. Enter new employee')
    print('2. List all employees')
    print('3. Employee ID Search')
    print('4. Position Search')
    print('5. Exit')
    _choice = input('What would you like to do? [1, 2, 3, 4, 5]: ')
    if _choice == '5': exit()
    elif _choice == '4':
        _position = input('Enter the position to search: ').lower()
        position_lookup = tb1.find(position=_position)
        if position_lookup:
            print(f'\nPosition: {_position}\n')
            print('------------------------')
            for emp in position_lookup:
                print('\n  Employee No.', emp['employee_id'])
                print('')
                print(f"   {emp['first_name']} {emp['last_name']}")
                print('   E-Mail - ', emp['email'])
                print('   Position:', emp['position'])
                print('   Date Added:', emp['created'])
                print('')
                print('------------------------')
            main()
        else:
            print('\nPosition not found.\n')
            main()
    elif _choice == '3':
        _eid = int(input('Enter Employee ID number: '))
        id_lookup = tb1.find(employee_id=_eid)
        if id_lookup:
            for emp in id_lookup:
                print('------------------------')
                print('\n  Employee ID: ', emp['employee_id'])
                print('')
                print(f"   {emp['first_name']} {emp['last_name']}")
                print('   E-Mail - ', emp['email'])
                print('   Position:', emp['position'])
                print('   Date Added:', emp['created'])
                print('')
                print('------------------------')
            main()
        else:
            print('\nEmployee ID not found.\n')
            main()
    elif _choice == '2':
        print('------------------------')
        for emp in tb1.get_all():
            print('\n  Employee ID:', emp['employee_id'])
            print('')
            print(f"   {emp['first_name']} {emp['last_name']}")
            print('   E-Mail - ', emp['email'])
            print('   Position:', emp['position'])
            print('   Date Added:', emp['created'])
            print('')
            print('------------------------')
        main()
    elif _choice == '1':
        # New Employee Information
        _first = input('First Name: ')
        _last  = input('Last Name: ')
        _email = input('E-Mail: ')
        _pos   = input('Position: ')
        new_id = new_employee(db, tb1, _first, _last, _email, _pos)
        db.load(_DB_FILE)
        tb1: pytb = db[_TB_NAME]
        new_info = tb1.find(employee_id=new_id)[0]
        print('------------------------')
        print('  Employee No.', new_info['employee_id'])
        print('')
        print(f"   {new_info['first_name']} {new_info['last_name']}")
        print('   E-Mail - ', new_info['email'])
        print('   Position:', new_info['position'])
        print('------------------------\n')
        main()
    else:
        print("\nNot a valid option\n")
        main()

if __name__ == '__main__':
    main()
