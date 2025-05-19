# Parking System
import sys 
sys.path.insert(0, 'options')
from new_parking import new_parking
print("-------------------Parking system-------------------")
print("Welcome to the Parking system! What would you like to do today?")
print("1. New parking")
print("2. View vehicle")

choice = input("Enter your choice (1 or 2): ")
if choice == "1":
    new_parking()
