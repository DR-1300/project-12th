
def new_parking():
    print("You chose to create a new parking.")
    number_plate = input("Enter the vehicle number plate: ")
    vehicle_type = input("Enter the vehicle type (car, bike, etc.): ")
    parking_spot = input("Enter the parking spot number: ")
    print(f"New parking created for vehicle {number_plate} of type {vehicle_type} at spot {parking_spot}.")
