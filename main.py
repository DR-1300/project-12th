# A parking management system made by me :p
import mysql.connector
import time
from datetime import datetime

global conn,cursor

conn = mysql.connector.connect(host='localhost', user='root',password='mysql123',database='parking_system')


cursor = conn.cursor()
def clear():
    for i in range(50):
        print()

def login():
    while True:
        clear()
        username = input('Enter your id :')
        userpass = input('Enter your Password :')
        cursor.execute('select * from users where username = "{}" and password = "{}"'.format(username, userpass))
        cursor.fetchall()
        rows = cursor.rowcount
        if rows != 1:
            print('Invalid username or password. Please try again')
        elif rows==1:
            print('Welcome :) you now have access to operate this system!')
            print('\n\n\n')
            print('Please press the "Enter Key" to continue')
            break
        else:
            print("somethings wrong i can feel it")


def vehicle_enter():
    clear()
    print("Vehicle Entry")
    print("=============")
    vehicle_no = input("Enter Vehicle Number: ").upper()
    vehicle_type = int(input("Enter Vehicle Type ( 1. Car, 2. Bus, 3. Bike ): "))
    entry_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if vehicle_type not in [1,2,3]:
        print("Invalid vehicle type.") 
        return
    cursor.execute("SELECT COUNT(*) FROM log WHERE exited_at IS NULL")
    coun = cursor.fetchone()[0]
    if coun >=10:
        print("Parking Full. Cannot accommodate more vehicles.")
        return
    else:
        cursor.execute("INSERT INTO log (vehicle_type, entered_at, vehicle_id) VALUES (%s, %s, %s)", 
                   (vehicle_type, entry_time, vehicle_no))
        cursor.execute("UPDATE statistics SET total_vehicles_ever = total_vehicles_ever + 1 WHERE total_slots = 10")
        conn.commit()
        cursor.execute("SELECT parking_id FROM log WHERE vehicle_id = %s AND entered_at = %s", (vehicle_no, entry_time))
        parking_id = cursor.fetchone()[0]
        print(f"Vehicle {vehicle_no} of type {vehicle_type} entered at {entry_time}.\n Parking ID: {parking_id}")
        cursor.execute("SELECT slot_id FROM parking_slots WHERE status = 'empty' LIMIT 1")
        slot = cursor.fetchone()
        cursor.execute("UPDATE parking_slots SET status = 'occupied', vehicle_id = %s, parking_id = %s WHERE slot_id = %s", (vehicle_no, parking_id, slot[0]))
        conn.commit()
    input("Press Enter to return to the main menu...")
def vehicle_exit():
    clear()
    print("Vehicle Exit")
    print("============")
    parking_id = int(input("Enter Parking ID: "))
    exit_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute(
        "SELECT vehicle_type, entered_at FROM log WHERE parking_id = %s AND exited_at IS NULL",
        (parking_id,)
    )
    record = cursor.fetchone()

    if record is None:
        print("Invalid Parking ID or Vehicle already exited.")
        return

    vehicle_type, entered_at = record
    cursor.execute(
        "SELECT TIMESTAMPDIFF(HOUR, %s, %s)",
        (entered_at, exit_time)
    )
    hours_stayed = cursor.fetchone()[0]

    if hours_stayed == 0:
        hours_stayed = 1 
    rates = {1: 50, 2: 100, 3: 25} 
    fee = hours_stayed * rates.get(vehicle_type, 50)

    cursor.execute(
        "UPDATE log SET exited_at = %s, money = %s WHERE parking_id = %s",
        (exit_time, fee, parking_id)
    )
    conn.commit()

    cursor.execute(
        "UPDATE statistics SET total_money = total_money + %s WHERE total_slots = 10",
        (fee,)
    )
    conn.commit()
    cursor.execute(
        "UPDATE parking_slots SET status = 'empty', vehicle_id = NULL, parking_id = NULL WHERE parking_id = %s",
        (parking_id,)
    )
    conn.commit()

    print(f"Vehicle of type {vehicle_type} exited at {exit_time}.")
    print(f"Duration: {hours_stayed} hour(s), Fee: ₹{fee}")
    input("Press Enter to return to the main menu...")

def show_statistics():
    clear()
    print("Parking Statistics")
    print("==================")
    cursor.execute("SELECT total_money, total_vehicles_ever FROM statistics WHERE total_slots = 10")
    stats = cursor.fetchone()
    if stats:
        total_money, total_vehicles = stats
    else:
        total_money, total_vehicles = 0, 0

    cursor.execute("SELECT COUNT(*) FROM log WHERE exited_at IS NULL AND entered_at IS NOT NULL")
    current_vehicles = cursor.fetchone()[0]
    print(f"Total Money Collected: ₹{total_money}")
    print(f"Total Vehicles Parked ever: {total_vehicles}")
    print(f"Current Vehicles in Parking: {current_vehicles}")
    input("Press Enter to return to the main menu...")

def free_slots():
    clear()
    print("Free Parking Slots")
    print("==================")
    cursor.execute("SELECT COUNT(*) FROM log WHERE exited_at IS NULL AND entered_at IS NOT NULL")
    occupied_slots = cursor.fetchone()[0]
    total_slots = 10
    free_slots = total_slots - occupied_slots
    print(f"Total Slots: {total_slots}")
    print(f"Occupied Slots: {occupied_slots}")
    print(f"Free Slots: {free_slots}")
    cursor.execute("SELECT slot_id FROM parking_slots WHERE status = 'empty'")
    freeslotrecords = cursor.fetchall()
    print("Free Slot IDs:")
    for i in freeslotrecords:
        print(f"- Slot {i[0]}")
    input("Press Enter to return to the main menu...")

def slot_status():
    slot_id = int(input("Enter Slot ID to check status (1-10): "))
    
    cursor.execute("SELECT status FROM parking_slots WHERE slot_id = %s", (slot_id,))
    result = cursor.fetchone()

    if result is None:
        print(f"Slot {slot_id} does not exist.")
    else:
        print(f"Slot {slot_id} is currently {result[0]}.")
    input("Press Enter to return to the main menu...")

def main_menu():
    clear()
    login()
    clear()
    while True: 
        clear()
        print('PARKING MANAGEMENT SYSTEM')
        print('*' * 100)
        print("\n1. Vehicle entered")
        print("\n2. Vehicle Exit")
        print("\n3. Show Parking Statistics")
        print("\n4. Show Free Parking Slots")
        print("\n5. Check Slot Status")
        print("\n6. Exit")
        try:
            choice = int(input('Enter your choice....!: '))
        except ValueError:
            print("Please enter a valid number.")
            continue


        if choice == 1:
            vehicle_enter()
        if choice == 2:
            vehicle_exit()
        if choice == 3:
            show_statistics()
        if choice == 4:
            free_slots()
        if choice == 5:
            slot_status()
        if choice == 6:
            print('Thank you for using the Parking Management System. Goodbye!')
            break
        else:
            print('Invalid choice. Please try again.')

if __name__ == "__main__":
    main_menu()
