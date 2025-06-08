# Parkking system 
import mysql.connector
import time
from datetime import datetime

global conn,cursor

conn = mysql.connector.connect(host='localhost', user='root',password='mysql123',database='parking_system')


cursor = conn.cursor()
def clear():
    for i in range(50):
        print()

def display_parking_type_records():
    cursor.execute('select * from parking_type;')
    records = cursor.fetchall()
    for row in records:
        print(row)
def display_parking_slot_records():
    cursor.execute('select * from parking_space;')
    records = cursor.fetchall()
    for row in records:
        print(row)
def login():
    while True:
        clear()
        username = input('Enter your id :')
        userpass = input('Enter your Password :')
        cursor.execute('select * from login where name = "{}" and password = "{}"'.format(username, userpass))
        cursor.fetchall()
        rows = cursor.rowcount
        if rows != 1:
            print('Invalid username or password................... Please try again!')
        else:
            print('Welcome :) you now have access to operate this system!')
            print('\n\n\n')
            print('Please press the "Enter Key" to continue')
            break
def add_parking_slot_record():
    clear()
    parking_type_id = input('Enter The Parking Type Number (1) Two Wheelar 2) Car 3) Bus 4) Truck 5) Trolly):')
    status = input('Enter The Current Status(Open/Full);')
    sql = 'insert into parking_space(type_id,status) values({},"{}");'.format(parking_type_id,status)
    cursor.execute(sql)
    conn.commit()
    print('\n\n The New Parking Space Record has been added......!')
    cursor.execute('select max(id) from parking_space;')
    no = cursor.fetchone()
    print('Your Parking ID is:{}\n\n\n'.format(no[0]))
    wait = input('\n\n\nReady? Press any key to countinue....')

def add_parking_type_record():
    clear()
    name = input('Enter Parking Type(1. Two Wheeler 2. Car 3. Bus 4. Truck 5. Trolly):')
    price = input('Enter Parking Price per Day:')
    sql = 'insert into parking_type(name,price) values("{}",{});'.format(name,price)
    cursor.execute(sql)
    conn.commit()
    print('\n\n New Parking Type added...')
    cursor.execute('select max(id) from parking_type')
    no = cursor.fetchone()
    print('New Parking Type ID is:{}\n\n\n'.format(no[0]))
    wait = input('\n\n\nPress any key to continue.........')

def add_new_vehicle():
    clear()
    print('Vehicle Login Screen')
    print('-'*100)
    vehicle_id = input('Enter Vehicle Number :')
    parking_id = input('Enter parking ID :')
    entry_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    sql = 'insert into transaction(vehicle_id,parking_id,entry_date) values ("{}",{},"{}");'.format(vehicle_id,parking_id,entry_date)
    cursor.execute(sql)
    cursor.execute('update parking_space set status="full" where id={}'.format(parking_id))
    print('\n\n\n Record has been added successfully.......!')
    wait = input('\n\n\nReady?Now press any key to countinue.....')
    conn.commit()

def remove_vehicle():
    clear()
    print('Vehicle Logout Screen')
    print('-'*100)
    vehicle_id=input('Enter vehicle No:')
    exit_date = datetime.today()
    sql='select * from transaction tr,parking_space ps,parking_type pt where tr.parking_id = ps.id and ps.type_id = pt.id and vehicle_id = "'+vehicle_id+'" and exit_date is Null;'
    cursor.execute(sql)
    record=cursor.fetchone()
    days=(exit_date-record[2]).days
    if days ==0:
        days=days+1
    amount=record[1]*days
    clear()
    print('Logout Details ')
    print('_'*100)
    print('Parking ID : {}'.format(record[0]))
    print('Vehicle ID : {}'.format(vehicle_id))
    print('Parking Date : {}'.format(record[2]))
    print('Current Date : {}'.format(exit_date))
    print('Amount Payable : {}'.format(amount))
    wait=input('Okay ready? Now Press any key to continue.........!')
    sql1 = 'update transaction set exit_date = "{}" , amount = {} where vehicle_id = "{}" and exit_date is NULL;'.format(exit_date,amount, vehicle_id)
    sql2='update parking_space set status = "open" where id = {}'.format(record[0])
    cursor.execute(sql1)
    cursor.execute(sql2)
    wait=input('The vehicle has been successfully removed from our system........\n Press any key to continue.......')


def modify_parking_type_record():
    clear()
    print('M O D I F Y  P A R K I N G  T Y P E  S C R E E N')
    print('-'*100)
    print('1. Parking Type Name \n')
    print('2. Parking Price \n')
    choice=int(input('Enter your choice:'))
    field=''
    if choice == 1:
        field='name'
    if choice == 2:
        field='price'

    park_id=input('Enter Parking Type ID:')
    value=input('Enter new values:')
    sql='update parking_type set '+ field+'="'+ value +'" where id='+ park_id+';'
    cursor.execute(sql)
    print('Record updated successfully.............')
    display_parking_type_records()
    wait=input('\n\n\nPress any key to continue..........')
    conn.commit() 

def modify_parking_space_record():
    clear()
    print('M O D I F Y  P A R K I N G  S P A C E  R E C O R D')
    print('-'*100)
    print('1. Parking Type ID(1-Two Wheeler, 2: Car 3.Bus etc):')
    print('2. status \n')
    choice = int(input('Enter your choice:'))
    field=''
    if choice == 1:
        field= 'type_id'
    if choice == 2:
        field='status'
    print('\n\n\n')
    crime_id=input('Enter Parking space ID:')
    value=input(('Enter new values:'))
    sql='update parking_space set ' + field +'="'+ value +'"where id='+ crime_id +';'
    cursor.execute(sql)
    print('Record updated successfully..............')
    wait=input('\n\n\nPress any key to continue..........')
    conn.commit()

def search_menu():
    clear()
    print(' SEARCH PARKING MENU')
    print('1)   Parking ID \n')
    print('2)   Vehicle Parked \n')
    print('3)   Free Space \n')
    choice = int(input('Enter you choice :'))
    field = ' '
    if choice == 1:
        field = 'id'
    if choice == 2:
        field = 'vehicle No'
    if choice == 3:
        field = 'status'
    value = input('Enter value to search :')
    if choice == 1 or choice == 3:
        sql = (
    'SELECT ps.id, name, price, status '
    'FROM parking_space ps, parking_type pt '
    'WHERE ps.id = pt.id AND ps.id = {}'.format(value)
)
    else:
        sql = '''
    SELECT id, vehicle_id, parking_id, entry_date 
    FROM transaction 
    WHERE exit_date IS NULL;
'''
    cursor.execute(sql)
    results = cursor.fetchall()
    records = cursor.rowcount
    for row in results:
        print(row)
    if records < 1:
        print('Record not found \n\n\n ')
    wait = input('\n\n\nOkay ready??? Now click on any key to continue.......!')

def parking_status(status):
    clear()
    print('Parking Status :',status)
    print('_'*100)
    sql = "select * from parking_space where status ='{}'".format(status)
    cursor.execute(sql)
    records = cursor.fetchall()
    for row in records:
        print(row)
    wait = input('\n\n\nOkay now are you ready??? click any key to continue.......!')

def vehicle_status_report():
    clear()
    print('Vehicle Status - Currently parked')
    print('_'*100)
    sql = 'select * from transaction where exit_date is NULL;'
    cursor.execute(sql)
    records = cursor.fetchall()
    for row in records:
        print(row)
    wait = input('\n\n\nOkay now ready??? Click on any key to continue......!')

def money_collection():
    clear()
    start_date = input('Enter starting Date(yyyy-mm-dd):  ')
    end_date = input('Enter End Date(yyyy-mm-dd):  ')
    sql = "select sum(amount) from transaction where \
              entry_date ='{}' and exit_date ='{}'".format(start_date,end_date)
    cursor.execute(sql)
    result = cursor.fetchone()
    clear()
    print('Total money Collected form {} to {}'.format(start_date,end_date))
    print('-'*100)
    print(result[0])
    wait = input('\n\n\nReady? Press any key to continue.....!')

def report_menu():
    while True:
        clear()
        print('Parking Space System')
        print('-'*100)
        print('1. Parking types \n')
        print('2. Free Space \n')
        print('3. Occupied Space \n')
        print('4. Vehicle status \n')
        print('5. Money Collected \n')
        print('6. Exit \n')
        choice=int(input('Enter your choice:'))
        field=''
        if choice == 1:
            display_parking_type_records()
        if choice == 2:
            parking_status("open")
        if choice == 3:
            parking_status("full")
        if choice == 4:
            vehicle_status_report()
        if choice == 5:
            money_collection()
        if choice == 6:
            break
        
def main_menu():
    clear()
    login()
    clear()
    while True: 
        clear()
        print('PARKING MANAGEMENT SYSTEM')
        print('*' * 100)
        print("\n1.   Add New Parking Type")
        print("\n2.  Add New Parking Slot")
        print('\n3.   Modify Parking Type Record')
        print('\n4.   Modify Parking Slot Record')
        print('\n5.   Vehicle Login')
        print('\n6.   Vehicle Logout')
        print('\n7.   Search menu')
        print('\n8.   Report menu')
        print('\n9.   Close application')
        print('\n\n')
        try:
            choice = int(input('Enter your choice....!: '))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if choice == 1:
            add_parking_type_record()
        if choice == 2:
            add_parking_slot_record()
        if choice == 3:
            modify_parking_type_record()
        if choice == 4:
            modify_parking_space_record()
        if choice == 5:
            add_new_vehicle()
        if choice == 6:
            remove_vehicle()
        if choice == 7:
            search_menu()
        if choice == 8:  
            report_menu()
        if choice == 9:
            conn.close()
            print('Thank you for using the Parking Management System. Goodbye!')
            break
        

if __name__ == "__main__":
    main_menu()