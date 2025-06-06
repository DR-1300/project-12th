# Parkking system 
import mysql.connector
import time
from datetime import datetime

global conn, cursor

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

def main_menu():
    clear()
    login()
    clear()
    while True:
        clear()
        print('Welcome to the Parking System')
        print('1. Add Parking Type Record')
        print('2. Add Parking Slot Record')
        print('3. Display Parking Type Records')
        print('4. Add New Vehicle')
        print('5. Exit')
        choice = input('Enter your choice: ')
        
        if choice == '1':
            add_parking_type_record()
        elif choice == '2':
            add_parking_slot_record()
        elif choice == '3':
            display_parking_type_records()
            input('\n\nPress any key to continue...')
        elif choice == '4':
            add_new_vehicle()
        elif choice == '5':
            print('Exiting the system. Goodbye!')
            cursor.close()
            conn.close()
            break
        else:
            print('Invalid choice, please try again.')
if __name__ == "__main__":
    main_menu()